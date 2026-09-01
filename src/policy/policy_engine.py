from typing import Dict, Any, Optional, List
from src.policy.thresholds import GuardrailAction, PolicyConfig

class PolicyDecision:
    def __init__(self, action: GuardrailAction, risk_score: float, reason: str, metadata: Optional[Dict[str, Any]] = None):
        self.action = action
        self.risk_score = risk_score
        self.reason = reason
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action.value,
            "risk_score": self.risk_score,
            "reason": self.reason,
            "metadata": self.metadata
        }


class PolicyEngine:
    """Decoupled decision engine converting raw classifier probability into actionable security decisions."""

    def __init__(self, config: Optional[PolicyConfig] = None):
        self.config = config or PolicyConfig()
        self.allowlist_phrases: List[str] = [
            "how to prevent prompt injection",
            "explain what a jailbreak is in security",
            "what is deberta-v3",
            "owasp top 10 for llm"
        ]

    def evaluate(self, prompt: str, classifier_score: float) -> PolicyDecision:
        clean_prompt = prompt.strip().lower()

        # 1. Allowlist evaluation (Educational/Benign bypass)
        if self.config.allowlist_enabled:
            for phrase in self.allowlist_phrases:
                if phrase in clean_prompt:
                    return PolicyDecision(
                        action=GuardrailAction.ALLOW,
                        risk_score=classifier_score,
                        reason="Matched trusted benign allowlist pattern.",
                        metadata={"allowlisted": True}
                    )

        # 2. Probability Threshold Decisions
        if classifier_score >= self.config.block_threshold:
            return PolicyDecision(
                action=GuardrailAction.BLOCK,
                risk_score=classifier_score,
                reason=f"High risk score ({classifier_score:.3f} >= {self.config.block_threshold:.2f}). Prompt blocked.",
                metadata={"threshold_violation": "BLOCK"}
            )
        elif classifier_score >= self.config.review_threshold:
            return PolicyDecision(
                action=GuardrailAction.REVIEW,
                risk_score=classifier_score,
                reason=f"Suspicious risk score ({classifier_score:.3f} in [{self.config.review_threshold:.2f}, {self.config.block_threshold:.2f})). Flagged for review.",
                metadata={"threshold_violation": "REVIEW"}
            )
        else:
            return PolicyDecision(
                action=GuardrailAction.ALLOW,
                risk_score=classifier_score,
                reason=f"Low risk score ({classifier_score:.3f} < {self.config.review_threshold:.2f}). Safe to execute.",
                metadata={"threshold_violation": "NONE"}
            )
