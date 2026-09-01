import time
from typing import Tuple, Optional
from src.models.classifier import BaseGuardrailClassifier
from src.policy.policy_engine import PolicyEngine, PolicyDecision
from src.policy.thresholds import GuardrailAction
from src.llm.provider import BaseLLMProvider

class GuardrailMiddleware:
    """Orchestrates Classifier scoring, Policy Engine decisions, and downstream LLM forwarding."""

    def __init__(
        self,
        classifier: BaseGuardrailClassifier,
        policy_engine: PolicyEngine,
        llm_provider: BaseLLMProvider
    ):
        self.classifier = classifier
        self.policy_engine = policy_engine
        self.llm_provider = llm_provider

    async def process_prompt(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Tuple[PolicyDecision, Optional[str], float]:
        """Executes the full defensive inspection pipeline and returns (decision, llm_response, latency_ms)."""
        start_time = time.perf_counter()

        # 1. Compute Classifier risk score
        scores = self.classifier.predict_score(prompt)
        risk_score = float(scores[0]) if scores else 0.0

        # 2. Evaluate Policy Decision
        decision = self.policy_engine.evaluate(prompt, risk_score)
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        # 3. Conditional Forwarding to Downstream LLM
        llm_response = None
        if decision.action in (GuardrailAction.ALLOW, GuardrailAction.REVIEW):
            llm_response = await self.llm_provider.generate(prompt, system_prompt)

        return decision, llm_response, latency_ms
