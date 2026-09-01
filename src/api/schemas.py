from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class GuardrailCheckRequest(BaseModel):
    prompt: str = Field(..., description="User prompt to inspect", json_schema_extra={"example": "What is the capital of France?"})
    system_prompt: Optional[str] = Field(None, description="Optional system instruction")
    llm_target: Optional[str] = Field("mock", description="Downstream LLM target (mock, openai, gemini, groq)")


class GuardrailCheckResponse(BaseModel):
    action: str = Field(..., description="Decision: ALLOW, REVIEW, or BLOCK")
    allowed: bool = Field(..., description="Whether the prompt was allowed through to the LLM")
    risk_score: float = Field(..., description="Probability of malicious injection (0.0 to 1.0)")
    reason: str = Field(..., description="Explanation of policy decision")
    latency_ms: float = Field(..., description="Guardrail inspection latency in milliseconds")
    llm_response: Optional[str] = Field(None, description="Downstream LLM generation if allowed")
    metadata: Optional[Dict[str, Any]] = None
