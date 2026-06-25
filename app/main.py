import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes import summarize, translate, generate_email
from app.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

# ── App Setup ──────────────────────────────────────────
app = FastAPI(
    title=os.getenv("APP_NAME", "IR INFOTECH API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="""
## AI-Powered REST API

Built with **FastAPI** using **Google Gemini** as primary AI and **Groq** as fallback.

### Available Endpoints
- **POST /summarize** — Summarize long text
- **POST /translate** — Translate text to any language  
- **POST /generate-email** — Generate professional emails
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── CORS Middleware ────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global Exception Handler ───────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc), "status_code": 500}
    )

# ── Routes ─────────────────────────────────────────────
app.include_router(summarize.router, tags=["Summarize"])
app.include_router(translate.router, tags=["Translate"])
app.include_router(generate_email.router, tags=["Generate Email"])

# ── Health Check ───────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "running",
        "app": os.getenv("APP_NAME", "IR INFOTECH API"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
