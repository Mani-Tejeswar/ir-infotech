"""
Basic API tests for IR INFOTECH API.
Run with: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

LONG_TEXT = (
    "Artificial intelligence is rapidly transforming industries worldwide. "
    "From healthcare to finance, AI is being used to analyze data, automate "
    "processes, and make accurate predictions. Machine learning enables computers "
    "to learn from data without being explicitly programmed for each task."
)


# ── Health Checks ──────────────────────────────────────
class TestHealth:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "running"

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


# ── Summarize ──────────────────────────────────────────
class TestSummarize:
    def test_valid_request(self):
        response = client.post("/summarize", json={
            "text": LONG_TEXT,
            "max_words": 50
        })
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "word_count" in data
        assert "provider" in data
        assert data["provider"] in ["gemini", "groq"]

    def test_text_too_short_returns_422(self):
        response = client.post("/summarize", json={
            "text": "Too short",
            "max_words": 50
        })
        assert response.status_code == 422

    def test_missing_text_returns_422(self):
        response = client.post("/summarize", json={"max_words": 50})
        assert response.status_code == 422

    def test_max_words_out_of_range_returns_422(self):
        response = client.post("/summarize", json={
            "text": LONG_TEXT,
            "max_words": 10   # below minimum of 50
        })
        assert response.status_code == 422


# ── Translate ──────────────────────────────────────────
class TestTranslate:
    def test_valid_request(self):
        response = client.post("/translate", json={
            "text": "Hello, how are you?",
            "target_language": "French"
        })
        assert response.status_code == 200
        data = response.json()
        assert "translated_text" in data
        assert "target_language" in data
        assert data["target_language"] == "French"

    def test_missing_target_language_returns_422(self):
        response = client.post("/translate", json={
            "text": "Hello"
        })
        assert response.status_code == 422

    def test_empty_text_returns_422(self):
        response = client.post("/translate", json={
            "text": "",
            "target_language": "Spanish"
        })
        assert response.status_code == 422


# ── Generate Email ─────────────────────────────────────
class TestGenerateEmail:
    def test_valid_request(self):
        response = client.post("/generate-email", json={
            "purpose": "Request a meeting to discuss the project timeline and deliverables",
            "recipient_name": "Project Manager",
            "sender_name": "Mani Tejeswar",
            "tone": "professional"
        })
        assert response.status_code == 200
        data = response.json()
        assert "subject" in data
        assert "body" in data
        assert "provider" in data

    def test_purpose_too_short_returns_422(self):
        response = client.post("/generate-email", json={
            "purpose": "Meeting"   # below min_length of 10
        })
        assert response.status_code == 422

    def test_missing_purpose_returns_422(self):
        response = client.post("/generate-email", json={
            "recipient_name": "Manager"
        })
        assert response.status_code == 422

    def test_optional_fields_work(self):
        response = client.post("/generate-email", json={
            "purpose": "Follow up on the submitted application status"
        })
        assert response.status_code == 200
