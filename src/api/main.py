from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os

from src.api.schemas import GuardrailCheckRequest, GuardrailCheckResponse
from src.api.middleware import GuardrailMiddleware
from src.models.classifier import TfidfBaselineClassifier, DummyClassifier
from src.policy.policy_engine import PolicyEngine
from src.policy.thresholds import PolicyConfig, GuardrailAction
from src.llm.provider import get_llm_provider, MockLLMProvider, OpenAILLMProvider, GeminiLLMProvider, GroqCloudLLMProvider
from src.utils.logger import get_logger


logger = get_logger("pi_guard.api")
middleware_instance: GuardrailMiddleware = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global middleware_instance
    logger.info("Initializing PI-Guard Service...")
    
    # Initialize Classifier
    model_path = os.getenv("BASELINE_MODEL_PATH", "models/baseline/baseline_tfidf.joblib")
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
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PI-Guard"}

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
