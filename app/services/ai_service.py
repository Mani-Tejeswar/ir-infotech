import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq
from app.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

# ── Configure Clients ──────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

GEMINI_MODEL = "gemini-1.5-flash"
GROQ_MODEL   = "llama3-8b-8192"


# ── Core AI caller with fallback ───────────────────────
def call_ai(prompt: str) -> tuple[str, str]:
    """
    Returns (response_text, provider_name)
    Tries Gemini first, falls back to Groq.
    """
    # Try Gemini
    try:
        logger.info("Calling Gemini...")
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        logger.info("Gemini responded successfully.")
        return response.text.strip(), "gemini"
    except Exception as e:
        logger.warning(f"Gemini failed: {e}. Falling back to Groq...")

    # Fallback to Groq
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
        raise RuntimeError("Both Gemini and Groq are unavailable.") from e


# ── Task Functions ─────────────────────────────────────
def summarize_text(text: str, max_words: int = 150) -> tuple[str, str]:
    prompt = (
        f"Summarize the following text in no more than {max_words} words. "
        f"Be concise and capture the key points.\n\nText:\n{text}"
    )
    return call_ai(prompt)


def translate_text(text: str, target_language: str, source_language: str = "auto") -> tuple[str, str]:
    src = "auto-detect the source language and" if source_language == "auto" else f"from {source_language}"
    prompt = (
        f"Translate the following text {src} to {target_language}. "
        f"Return ONLY the translated text, nothing else.\n\nText:\n{text}"
    )
    return call_ai(prompt)


def generate_email(
    purpose: str,
    recipient_name: str = None,
    sender_name: str = None,
    tone: str = "professional",
    additional_context: str = None
) -> tuple[str, str, str]:
    recipient = f"to {recipient_name}" if recipient_name else ""
    sender = f"from {sender_name}" if sender_name else ""
    context = f"\nAdditional context: {additional_context}" if additional_context else ""

    prompt = (
        f"Write a {tone} email {recipient} {sender} for the following purpose: {purpose}.{context}\n\n"
        f"Return the response in this exact format:\n"
        f"SUBJECT: <email subject here>\n"
        f"BODY:\n<email body here>"
    )
    result, provider = call_ai(prompt)

    # Parse subject and body
    subject, body = "", result
    if "SUBJECT:" in result and "BODY:" in result:
        parts = result.split("BODY:", 1)
        subject = parts[0].replace("SUBJECT:", "").strip()
        body = parts[1].strip()

    return subject, body, provider
