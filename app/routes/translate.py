from fastapi import APIRouter, HTTPException
from app.models.schemas import TranslateRequest, TranslateResponse
from app.services.ai_service import translate_text
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslateResponse,
    summary="Translate Text",
    description="Translates text to a target language using Gemini (falls back to Groq)."
)
async def translate(request: TranslateRequest):
    logger.info(f"POST /translate | target={request.target_language} | source={request.source_language}")
    try:
        translated, provider = translate_text(request.text, request.target_language, request.source_language)
        logger.info(f"Translated successfully via {provider}")
        return TranslateResponse(
            translated_text=translated,
            source_language=request.source_language,
            target_language=request.target_language,
            provider=provider
        )
    except RuntimeError as e:
        logger.error(f"Translate failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /translate: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
