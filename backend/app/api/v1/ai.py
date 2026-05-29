from fastapi import APIRouter, HTTPException

from ...core.config import settings
from ...schemas.ai import AIAskRequest, AIResponse, AISummarizeRequest

router = APIRouter(tags=["ai"])


@router.post("/ai/summarize", response_model=AIResponse)
async def summarize(request: AISummarizeRequest) -> AIResponse:
    # Guardrail: AI summarization is only a placeholder until a provider is configured.
    if settings.AI_PROVIDER == "disabled":
        raise HTTPException(status_code=503, detail="AI provider is not configured")
    return AIResponse(success=False, error="AI summarization is not enabled in this deployment.")


@router.post("/ai/ask", response_model=AIResponse)
async def ask(request: AIAskRequest) -> AIResponse:
    # Guardrail: No hallucination. Responses must be grounded in stored events and sources.
    if settings.AI_PROVIDER == "disabled":
        raise HTTPException(status_code=503, detail="AI provider is not configured")
    return AIResponse(success=False, error="AI question answering is not enabled in this deployment.")
