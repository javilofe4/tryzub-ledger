from pydantic import BaseModel


class AISummarizeRequest(BaseModel):
    event_id: int | None = None
    language_code: str = "en"
    prompt: str


class AIAskRequest(BaseModel):
    question: str
    language_code: str = "en"


class AIResponse(BaseModel):
    success: bool
    summary: str | None = None
    citations: list[str] = []
    error: str | None = None
