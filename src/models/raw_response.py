from pydantic import BaseModel
from typing import Optional, Any

class RawResponse(BaseModel):
    generated_text: str
    prompt_tokens: int
    response_tokens: int
    model_name: str
    metadata: Optional[Any] = None