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
