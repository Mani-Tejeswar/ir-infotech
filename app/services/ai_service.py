import os
from dotenv import load_dotenv
from groq import Groq
from app.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

# ── Configure Clients ──────────────────────────────────
# Primary: Google Gemini | Fallback: Groq
# NOTE: Gemini is configured but currently using Groq due to quota limits.
# To re-enable Gemini, set USE_GEMINI=true in .env
USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = "llama-3.1-8b-instant"

# Gemini setup (kept for when quota resets)
if USE_GEMINI:
    try:
        from google import genai as google_genai
        google_client = google_genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        GEMINI_MODEL = "models/gemini-1.5-flash"
        logger.info("Gemini client initialized.")
    except Exception as e:
        logger.warning(f"Gemini init failed: {e}. Will use Groq only.")
        USE_GEMINI = False


# ── Core AI caller with fallback ───────────────────────
def call_ai(prompt: str) -> tuple[str, str]:
    """
    Returns (response_text, provider_name)
    Tries Gemini first (if enabled), falls back to Groq.
    """
    # Try Gemini (if enabled)
    if USE_GEMINI:
        try:
            logger.info("Calling Gemini...")
            response = google_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            logger.info("Gemini responded successfully.")
            return response.text.strip(), "gemini"
        except Exception as e:
            logger.warning(f"Gemini failed: {e}. Falling back to Groq...")

    # Use Groq (fallback or primary)
    try:
        logger.info("Calling Groq...")
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        logger.info("Groq responded successfully.")
        return result, "groq"
    except Exception as e:
        logger.error(f"Groq also failed: {e}")
        raise RuntimeError("AI service is currently unavailable.") from e


# ── Task Functions ─────────────────────────────────────
def summarize_text(text: str, max_words: int = 150) -> tuple[str, str]:
    prompt = (
        f"You are an expert summarizer. Your task is to summarize the following text.\n\n"
        f"Instructions:\n"
        f"- Write a clear, concise summary in no more than {max_words} words.\n"
        f"- Capture all key points and main ideas.\n"
        f"- Use simple, professional language.\n"
        f"- Do NOT include phrases like 'This text discusses' or 'The article says'. Write directly.\n"
        f"- Return ONLY the summary, nothing else.\n\n"
        f"Text to summarize:\n{text}"
    )
    return call_ai(prompt)


def translate_text(text: str, target_language: str, source_language: str = "auto") -> tuple[str, str]:
    src = "auto-detect the source language" if source_language == "auto" else f"the source language is {source_language}"
    prompt = (
        f"You are a professional translator with expertise in multiple languages.\n\n"
        f"Instructions:\n"
        f"- Translate the text below to {target_language} ({src}).\n"
        f"- Preserve the original tone, style, and meaning accurately.\n"
        f"- Do NOT add explanations, notes, or extra commentary.\n"
        f"- Return ONLY the translated text, nothing else.\n\n"
        f"Text to translate:\n{text}"
    )
    return call_ai(prompt)


def generate_email(
    purpose: str,
    recipient_name: str = None,
    sender_name: str = None,
    tone: str = "professional",
    additional_context: str = None
) -> tuple[str, str, str]:
    recipient = f"The email is addressed to: {recipient_name}." if recipient_name else ""
    sender = f"The email is from: {sender_name}." if sender_name else ""
    context = f"Additional context: {additional_context}" if additional_context else ""

    prompt = (
        f"You are a professional email writer. Write a {tone} email for the following purpose.\n\n"
        f"Purpose: {purpose}\n"
        f"{recipient}\n"
        f"{sender}\n"
        f"{context}\n\n"
        f"Instructions:\n"
        f"- Write a complete, well-structured email with proper greeting and closing.\n"
        f"- Match the tone: {tone}.\n"
        f"- Keep it concise but comprehensive.\n"
        f"- Use proper email etiquette.\n\n"
        f"Return the response in EXACTLY this format (no extra text before or after):\n"
        f"SUBJECT: <subject line here>\n"
        f"BODY:\n<full email body here>"
    )
    result, provider = call_ai(prompt)

    # Parse subject and body
    subject, body = "", result
    if "SUBJECT:" in result and "BODY:" in result:
        parts = result.split("BODY:", 1)
        subject = parts[0].replace("SUBJECT:", "").strip()
        body = parts[1].strip()

    return subject, body, provider
