from enum import Enum
from pydantic import BaseModel, Field

class GuardrailAction(str, Enum):
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"

class PolicyConfig(BaseModel):
    block_threshold: float = Field(default=0.80, ge=0.0, le=1.0)
    review_threshold: float = Field(default=0.50, ge=0.0, le=1.0)
    enable_hard_keyword_filters: bool = True
    allowlist_enabled: bool = True
