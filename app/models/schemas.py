from pydantic import BaseModel, Field
from typing import Optional


# ── Summarize ──────────────────────────────────────────
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text to summarize (min 50 chars)")
    max_words: Optional[int] = Field(150, ge=50, le=500, description="Max words in summary")

class SummarizeResponse(BaseModel):
    summary: str
    word_count: int
    provider: str   # "gemini" or "groq"


# ── Translate ───────────────────────────────────────────
class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")
    target_language: str = Field(..., description="Target language e.g. 'French', 'Hindi'")
    source_language: Optional[str] = Field("auto", description="Source language (default: auto-detect)")

class TranslateResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    provider: str


# ── Generate Email ──────────────────────────────────────
class GenerateEmailRequest(BaseModel):
    purpose: str = Field(..., min_length=10, description="Purpose of the email")
    recipient_name: Optional[str] = Field(None, description="Recipient name")
    sender_name: Optional[str] = Field(None, description="Your name")
    tone: Optional[str] = Field("professional", description="Tone: professional, formal, friendly")
    additional_context: Optional[str] = Field(None, description="Extra context or details")

class GenerateEmailResponse(BaseModel):
    subject: str
    body: str
    provider: str


# ── Error ───────────────────────────────────────────────
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
