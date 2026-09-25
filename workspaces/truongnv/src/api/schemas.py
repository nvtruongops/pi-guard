from typing import Any

from pydantic import BaseModel, Field


class GuardrailCheckRequest(BaseModel):
    prompt: str = Field(..., description="User prompt to inspect", json_schema_extra={"example": "What is the capital of France?"})
    system_prompt: str | None = Field(None, description="Optional system instruction")
    llm_target: str | None = Field("mock", description="Downstream LLM target (mock, openai, gemini, groq)")


class GuardrailCheckResponse(BaseModel):
    action: str = Field(..., description="Decision: ALLOW, REVIEW, or BLOCK")
    allowed: bool = Field(..., description="Whether the prompt was allowed through to the LLM")
    risk_score: float = Field(..., description="Probability of malicious injection (0.0 to 1.0)")
    reason: str = Field(..., description="Explanation of policy decision")
    latency_ms: float = Field(..., description="Guardrail inspection latency in milliseconds")
    llm_response: str | None = Field(None, description="Downstream LLM generation if allowed")
    metadata: dict[str, Any] | None = None


class GuardrailInspectRequest(BaseModel):
    prompt: str = Field(..., description="Prompt or text document to inspect")
    max_chunk_size: int = Field(default=512, description="Token size for long document chunking")
    scan_strategy: str = Field(default="head_tail_priority", description="head_tail_priority or sequential")


class LatencyBreakdown(BaseModel):
    tier0_scrubber_ms: float = 0.0
    tier1_tfidf_ms: float = 0.0
    tier2_transformer_ms: float = 0.0
    total_ms: float = 0.0


class GuardrailInspectResponse(BaseModel):
    verdict: str = Field(..., description="ALLOW or BLOCK")
    resolved_at: str = Field(..., description="TIER_1_CLEARANCE, TIER_1_REJECTION, or TIER_2_ARBITRATION")
    final_score: float = Field(..., description="Confidence of maliciousness (0.0 to 1.0)")
    is_malicious: bool = Field(..., description="True if blocked")
    category: str = Field(default="BENIGN", description="Detected category")
    oov_density: float = Field(default=0.0, description="Out-of-vocabulary density")
    oov_escalation: bool = Field(default=False, description="Whether OOV gate forced escalation to Tier 2")
    latency: LatencyBreakdown
    flagged_chunk_index: int | None = None
    scanned_chunks: int | None = None
    total_chunks: int | None = None

