from fastapi import APIRouter, HTTPException
from app.models.schemas import GenerateEmailRequest, GenerateEmailResponse
from app.services.ai_service import generate_email
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/generate-email",
    response_model=GenerateEmailResponse,
    summary="Generate Email",
    description="Generates a professional email using Gemini (falls back to Groq)."
)
async def generate_email_route(request: GenerateEmailRequest):
    logger.info(f"POST /generate-email | purpose={request.purpose[:50]} | tone={request.tone}")
    try:
        subject, body, provider = generate_email(
            purpose=request.purpose,
            recipient_name=request.recipient_name,
            sender_name=request.sender_name,
            tone=request.tone,
            additional_context=request.additional_context
        )
        logger.info(f"Email generated successfully via {provider}")
        return GenerateEmailResponse(subject=subject, body=body, provider=provider)
    except RuntimeError as e:
        logger.error(f"Generate email failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /generate-email: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
