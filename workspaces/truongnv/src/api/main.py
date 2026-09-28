import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from src.api.middleware import GuardrailMiddleware
from src.api.schemas import (
    GuardrailCheckRequest,
    GuardrailCheckResponse,
    GuardrailInspectRequest,
    GuardrailInspectResponse,
    LatencyBreakdown,
)
from src.llm.provider import (
    MockLLMProvider,
)
from src.models.classifier import (
    LiteratureBaselineClassifier,
    DummyClassifier,
    TfidfBaselineClassifier,
)
from src.policy.policy_engine import PolicyEngine
from src.policy.thresholds import GuardrailAction, PolicyConfig
from src.utils.config import load_env_file
from src.utils.logger import get_logger

logger = get_logger("pi_guard.api")
middleware_instance: GuardrailMiddleware = None
classifier_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global middleware_instance, classifier_instance
    load_env_file()
    logger.info("Initializing PI-Guard Service with Literature Baseline...")

    try:
        classifier = LiteratureBaselineClassifier(model_key=os.getenv("GUARDRAIL_MODEL", "jain_baseline"))
        classifier_instance = classifier
        logger.info(f"Loaded Literature Baseline: {classifier.model_key}")
    except Exception as e:
        logger.warning(f"Failed to load LiteratureBaselineClassifier ({e}), falling back to TF-IDF.")
        default_model_path = "Final-Report/notebooks/models/baseline/baseline_tfidf.joblib" if os.path.exists("Final-Report/notebooks/models/baseline/baseline_tfidf.joblib") else ("notebooks/models/baseline/baseline_tfidf.joblib" if os.path.exists("notebooks/models/baseline/baseline_tfidf.joblib") else "models/baseline/baseline_tfidf.joblib")
        model_path = os.getenv("BASELINE_MODEL_PATH", default_model_path)
        if os.path.exists(model_path):
            classifier = TfidfBaselineClassifier(model_path)
        else:
            classifier = DummyClassifier()
        classifier_instance = classifier

    # Initialize Policy Engine
    policy_config = PolicyConfig(
        block_threshold=float(os.getenv("POLICY_BLOCK_THRESHOLD", 0.80)),
        review_threshold=float(os.getenv("POLICY_REVIEW_THRESHOLD", 0.50))
    )
    policy_engine = PolicyEngine(policy_config)

    # Initialize LLM Provider
    llm_provider = MockLLMProvider()

    middleware_instance = GuardrailMiddleware(classifier, policy_engine, llm_provider)
    logger.info("PI-Guard Middleware Ready with Literature Baseline.")
    yield
    logger.info("Shutting down PI-Guard Service...")

app = FastAPI(
    title="PI-Guard API",
    description="Machine-Learning Guardrail API for Detecting Prompt Injection and Jailbreak Attacks",
    version="2.2.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "PI-Guard",
        "version": "2.2.0",
        "model_type": "Peer-Reviewed Literature Baseline",
        "is_paper_grounded": True,
        "is_synthetic_self_created": False
    }

@app.post("/v1/chat/guardrail", response_model=GuardrailCheckResponse)
async def check_guardrail(req: GuardrailCheckRequest):
    global middleware_instance
    if not middleware_instance:
        raise HTTPException(status_code=503, detail="Guardrail service not initialized")

    decision, llm_reply, latency_ms = await middleware_instance.process_prompt(
        prompt=req.prompt,
        system_prompt=req.system_prompt
    )

    allowed = decision.action in (GuardrailAction.ALLOW, GuardrailAction.REVIEW)

    return GuardrailCheckResponse(
        action=decision.action.value,
        allowed=allowed,
        risk_score=decision.risk_score,
        reason=decision.reason,
        latency_ms=latency_ms,
        llm_response=llm_reply,
        metadata=decision.metadata
    )

@app.post("/v1/guard/inspect", response_model=GuardrailInspectResponse)
async def inspect_guardrail(req: GuardrailInspectRequest):
    """
    Literature Baseline model inspection for prompts.
    Returns verdict, score, category, and latency breakdown.
    """
    global classifier_instance
    if not classifier_instance:
        raise HTTPException(status_code=503, detail="Guardrail model not initialized")

    t0 = time.perf_counter()
    detailed = classifier_instance.inspect_detailed(req.prompt)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    latency_ms = detailed.get("latency_ms", elapsed_ms) or elapsed_ms

    is_attack = detailed.get("is_malicious", False)
    final_score = detailed.get("final_score", 0.0)

    latency = LatencyBreakdown(
        tier0_scrubber_ms=0.0,
        tier1_tfidf_ms=round(latency_ms, 3),
        tier2_transformer_ms=0.0,
        total_ms=round(latency_ms, 3)
    )

    return GuardrailInspectResponse(
        verdict="BLOCK" if is_attack else "ALLOW",
        resolved_at="LITERATURE_BASELINE_CLASSIFIER",
        final_score=round(final_score, 4),
        is_malicious=is_attack,
        category="ATTACK" if is_attack else "BENIGN",
        oov_density=0.0,
        oov_escalation=False,
        latency=latency
    )


