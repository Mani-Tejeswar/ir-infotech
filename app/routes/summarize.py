from fastapi import APIRouter, HTTPException
from app.models.schemas import SummarizeRequest, SummarizeResponse, ErrorResponse
from app.services.ai_service import summarize_text
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
    summary="Summarize Text",
    description="Summarizes the provided text using Gemini (falls back to Groq)."
)
async def summarize(request: SummarizeRequest):
    logger.info(f"POST /summarize | text_length={len(request.text)} | max_words={request.max_words}")
    try:
        summary, provider = summarize_text(request.text, request.max_words)
        word_count = len(summary.split())
        logger.info(f"Summarized successfully via {provider} | words={word_count}")
        return SummarizeResponse(summary=summary, word_count=word_count, provider=provider)
    except RuntimeError as e:
        logger.error(f"Summarize failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /summarize: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
