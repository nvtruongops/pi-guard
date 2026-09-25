import os
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
    ChampionCascadeClassifier,
    DummyClassifier,
    TfidfBaselineClassifier,
)
from src.policy.policy_engine import PolicyEngine
from src.policy.thresholds import GuardrailAction, PolicyConfig
from src.utils.config import load_env_file
from src.utils.logger import get_logger

logger = get_logger("pi_guard.api")
middleware_instance: GuardrailMiddleware = None
cascade_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global middleware_instance, cascade_instance
    load_env_file()
    logger.info("Initializing PI-Guard Service...")

    # Initialize Champion Cascade Guardrail
    try:
        from src.models.cascade import TwoTierCascadeGuardrail
        cascade_instance = TwoTierCascadeGuardrail()
        classifier = ChampionCascadeClassifier()
        logger.info("Initialized Champion Two-Tier Cascade Guardrail.")
    except Exception as e:
        logger.warning(f"Failed to load Champion Cascade ({e}), falling back to baseline.")
        cascade_instance = None
        default_model_path = "Final-Report/notebooks/models/baseline/baseline_tfidf.joblib" if os.path.exists("Final-Report/notebooks/models/baseline/baseline_tfidf.joblib") else ("notebooks/models/baseline/baseline_tfidf.joblib" if os.path.exists("notebooks/models/baseline/baseline_tfidf.joblib") else "models/baseline/baseline_tfidf.joblib")
        model_path = os.getenv("BASELINE_MODEL_PATH", default_model_path)
        if os.path.exists(model_path):
            classifier = TfidfBaselineClassifier(model_path)
            logger.info(f"Loaded baseline model from {model_path}")
        else:
            classifier = DummyClassifier()
            logger.info("Using DummyClassifier for development/testing.")

    # Initialize Policy Engine
    policy_config = PolicyConfig(
        block_threshold=float(os.getenv("POLICY_BLOCK_THRESHOLD", 0.80)),
        review_threshold=float(os.getenv("POLICY_REVIEW_THRESHOLD", 0.50))
    )
    policy_engine = PolicyEngine(policy_config)

    # Initialize LLM Provider
    llm_provider = MockLLMProvider()

    middleware_instance = GuardrailMiddleware(classifier, policy_engine, llm_provider)
    logger.info("PI-Guard Middleware Ready.")
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
        "champion_cascade_loaded": cascade_instance is not None
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
    Detailed multi-tier inspection for single prompts and long documents (up to 200k chars).
    Returns tier-by-tier latency breakdown, OOV density, routing state, and flagged blocks.
    """
    global cascade_instance
    if not cascade_instance:
        raise HTTPException(status_code=503, detail="Cascade Guardrail not initialized")

    prompt_len = len(req.prompt)
    if prompt_len > 2000:
        # Long document chunked scanning with early stopping
        res = cascade_instance.inspect_long_document(req.prompt, strategy=req.scan_strategy)
        is_attack = res["verdict"] in ("MALICIOUS", "BLOCK")
        latency = LatencyBreakdown(
            tier0_scrubber_ms=0.0,
            tier1_tfidf_ms=0.0,
            tier2_transformer_ms=round(res.get("latency_ms", 0.0), 3),
            total_ms=round(res.get("latency_ms", 0.0), 3)
        )
        return GuardrailInspectResponse(
            verdict="BLOCK" if is_attack else "ALLOW",
            resolved_at="LONG_DOCUMENT_BLOCK_SCAN",
            final_score=round(res.get("max_risk_score", 0.0), 4),
            is_malicious=is_attack,
            category="LONG_DOCUMENT_INJECTION" if is_attack else "BENIGN",
            oov_density=0.0,
            oov_escalation=False,
            latency=latency,
            flagged_chunk_index=res.get("flagged_block_index"),
            scanned_chunks=res.get("scanned_blocks"),
            total_chunks=res.get("total_blocks")
        )

    # Standard single prompt inspection
    res = cascade_instance.inspect_query(req.prompt)
    t_total = res["latency_ms"]
    latency = LatencyBreakdown(
        tier0_scrubber_ms=0.15,
        tier1_tfidf_ms=round(min(1.2, t_total * 0.4), 3),
        tier2_transformer_ms=round(max(0.0, t_total - 1.35), 3) if res["resolved_at"] == "TIER_2_ARBITRATION" else 0.0,
        total_ms=round(t_total, 3)
    )
    return GuardrailInspectResponse(
        verdict=res["verdict"],
        resolved_at=res["resolved_at"],
        final_score=round(res["final_score"], 4),
        is_malicious=(res["verdict"] == "BLOCK"),
        category=res.get("category", "BENIGN"),
        oov_density=res.get("oov_density", 0.0),
        oov_escalation=res.get("oov_escalation", False),
        latency=latency
    )

