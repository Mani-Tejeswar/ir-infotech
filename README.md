# IR INFOTECH API

A production-ready REST API built with **FastAPI** for AI-powered text processing. Uses **Google Gemini** as the primary AI provider with **Groq (LLaMA 3)** as automatic fallback.

---

## Features

- **POST /summarize** — Summarize long text into concise key points
- **POST /translate** — Translate text to any language
- **POST /generate-email** — Generate professional emails from a purpose description
- Automatic **Gemini → Groq fallback** if primary provider fails
- Request **validation** with Pydantic v2
- Structured **logging** to console and file
- **Environment variable** based configuration
- Auto-generated **Swagger UI** at `/docs`

---

## Project Structure

```
IR INFOTECH/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── routes/
│   │   ├── summarize.py     # POST /summarize
│   │   ├── translate.py     # POST /translate
│   │   └── generate_email.py# POST /generate-email
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response models
│   ├── services/
│   │   └── ai_service.py    # Gemini + Groq AI logic
│   └── utils/
│       └── logger.py        # Logging configuration
├── .env                     # Environment variables (not committed)
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Mani-Tejeswar/ir-infotech.git
cd ir-infotech
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
```
Edit `.env` and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
USE_GEMINI=false
GROQ_API_KEY=your_groq_api_key_here
APP_NAME=IR INFOTECH API
APP_VERSION=1.0.0
DEBUG=True
LOG_LEVEL=INFO
```

> Get Gemini API key: https://aistudio.google.com
> Get Groq API key: https://console.groq.com

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```

Server starts at: **http://127.0.0.1:8000**
Swagger Docs at: **http://127.0.0.1:8000/docs**

---

## API Documentation

### Health Check

#### `GET /`
```json
{
  "status": "running",
  "app": "IR INFOTECH API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### POST `/summarize`

Summarizes the provided text using AI.

**Request Body:**
```json
{
  "text": "Your long text here... (minimum 50 characters)",
  "max_words": 100
}
```

**Response:**
```json
{
  "summary": "AI-generated concise summary of the text.",
  "word_count": 45,
  "provider": "groq"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | ✅ | Text to summarize (min 50 chars) |
| `max_words` | integer | ❌ | Max words in summary (default: 150, range: 50–500) |

---

### POST `/translate`

Translates text to a target language.

**Request Body:**
```json
{
  "text": "Hello, how are you?",
  "target_language": "Hindi",
  "source_language": "auto"
}
```

**Response:**
```json
{
  "translated_text": "नमस्ते, आप कैसे हैं?",
  "source_language": "auto",
  "target_language": "Hindi",
  "provider": "groq"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | string | ✅ | Text to translate |
| `target_language` | string | ✅ | Target language (e.g. "French", "Hindi", "Telugu") |
| `source_language` | string | ❌ | Source language (default: "auto") |

---

### POST `/generate-email`

Generates a professional email based on a purpose description.

**Request Body:**
```json
{
  "purpose": "Request a meeting to discuss internship joining date",
  "recipient_name": "HR Manager",
  "sender_name": "Mani Tejeswar Reddy",
  "tone": "professional",
  "additional_context": "I received the offer letter last week"
}
```

**Response:**
```json
{
  "subject": "Request for Meeting – Internship Joining Date Confirmation",
  "body": "Dear HR Manager,\n\nI hope this message finds you well...",
  "provider": "groq"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `purpose` | string | ✅ | Purpose of the email (min 10 chars) |
| `recipient_name` | string | ❌ | Name of the recipient |
| `sender_name` | string | ❌ | Your name |
| `tone` | string | ❌ | Tone: `professional`, `formal`, `friendly` (default: professional) |
| `additional_context` | string | ❌ | Extra details for the AI |

---

## Error Handling

All errors return a consistent JSON format:

```json
{
  "detail": "Error description here"
}
```

| Status Code | Meaning |
|---|---|
| `422` | Validation error (invalid request body) |
| `500` | Internal server error |
| `503` | AI service unavailable (both Gemini and Groq failed) |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| Pydantic v2 | Request/Response validation |
| Google Gemini | Primary AI provider |
| Groq (LLaMA 3.1) | Fallback AI provider |
| python-dotenv | Environment variable management |
| Python Logging | Application logging |

---

## AI Provider Fallback Logic

```
Request → Try Gemini
             ↓ (if fails / quota exceeded)
          Try Groq
             ↓ (if fails)
          Return 503 error
```

Gemini can be enabled/disabled via `USE_GEMINI=true/false` in `.env`.

---

## Author

**Mani Tejeswar Reddy Avula**
Built for IR INFOTECH — Round 1 Internship Assessment
