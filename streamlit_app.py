import streamlit as st
import requests
import json

# ── Page Config ────────────────────────────────────────
st.set_page_config(
    page_title="IR INFOTECH AI Tools",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Styling ────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: #0f0f1a;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
    }

    .hero-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #7c3aed, #2563eb, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .result-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }

    .provider-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .badge-groq {
        background: rgba(5, 150, 105, 0.2);
        color: #10b981;
        border: 1px solid #10b981;
    }

    .badge-gemini {
        background: rgba(37, 99, 235, 0.2);
        color: #60a5fa;
        border: 1px solid #60a5fa;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 0.95rem;
    }

    div[data-testid="stTextArea"] textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px !important;
    }

    .stButton button {
        background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 0.6rem !important;
        transition: opacity 0.2s;
    }

    .stButton button:hover {
        opacity: 0.85 !important;
    }

    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://127.0.0.1:8000"


def check_api():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=2)
        return r.status_code == 200
    except:
        return False


def call_api(endpoint, payload):
    try:
        r = requests.post(f"{API_BASE}{endpoint}", json=payload, timeout=30)
        return r.status_code, r.json()
    except requests.exceptions.ConnectionError:
        return None, {"error": "Cannot connect to API. Make sure the server is running."}
    except Exception as e:
        return None, {"error": str(e)}


def provider_badge(provider):
    cls = "badge-groq" if provider == "groq" else "badge-gemini"
    icon = "⚡" if provider == "groq" else "✨"
    return f'<span class="provider-badge {cls}">{icon} {provider}</span>'


# ── Header ─────────────────────────────────────────────
st.markdown('<div class="hero-title">🤖 IR INFOTECH AI Tools</div>', unsafe_allow_html=True)

api_ok = check_api()
status_html = (
    '<div style="text-align:center;margin-bottom:2rem;">'
    f'<span class="status-dot"></span>'
    f'<span style="color:#94a3b8;font-size:0.85rem;">API {"Online" if api_ok else "Offline — start the server"}</span>'
    '</div>'
)
st.markdown(status_html, unsafe_allow_html=True)

if not api_ok:
    st.error("⚠️ FastAPI server is not running. Open a terminal and run: `uvicorn app.main:app --reload`")

# ── Tabs ───────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📝 Summarize", "🌐 Translate", "✉️ Generate Email"])


# ── Tab 1: Summarize ───────────────────────────────────
with tab1:
    st.markdown("### Summarize Text")
    st.markdown('<p style="color:#94a3b8;font-size:0.9rem;">Paste long text and get a concise summary.</p>', unsafe_allow_html=True)

    text_input = st.text_area("Text to summarize", height=200,
                              placeholder="Paste your long text here... (minimum 50 characters)")
    max_words = st.slider("Max words in summary", min_value=50, max_value=500, value=100, step=10)

    if st.button("✨ Summarize", key="btn_summarize"):
        if len(text_input.strip()) < 50:
            st.warning("Text must be at least 50 characters.")
        else:
            with st.spinner("Summarizing..."):
                status, data = call_api("/summarize", {"text": text_input, "max_words": max_words})

            if status == 200:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f'**Summary** &nbsp; {provider_badge(data["provider"])}', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#e2e8f0;margin-top:0.8rem;line-height:1.7;">{data["summary"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#64748b;font-size:0.8rem;">Word count: {data["word_count"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"Error: {data.get('detail') or data.get('error')}")


# ── Tab 2: Translate ───────────────────────────────────
with tab2:
    st.markdown("### Translate Text")
    st.markdown('<p style="color:#94a3b8;font-size:0.9rem;">Translate to any language instantly.</p>', unsafe_allow_html=True)

    translate_text = st.text_area("Text to translate", height=150,
                                  placeholder="Enter text to translate...")

    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox("Target Language", [
            "Hindi", "Telugu", "Tamil", "French", "Spanish", "German",
            "Arabic", "Japanese", "Chinese", "Portuguese", "Italian",
            "Russian", "Korean", "Bengali"
        ])
    with col2:
        source_lang = st.selectbox("Source Language", ["auto", "English", "Hindi", "French", "Spanish", "German"])

    if st.button("🌐 Translate", key="btn_translate"):
        if not translate_text.strip():
            st.warning("Please enter some text to translate.")
        else:
            with st.spinner(f"Translating to {target_lang}..."):
                status, data = call_api("/translate", {
                    "text": translate_text,
                    "target_language": target_lang,
                    "source_language": source_lang
                })

            if status == 200:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f'**Translation** ({source_lang} → {target_lang}) &nbsp; {provider_badge(data["provider"])}', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#e2e8f0;margin-top:0.8rem;font-size:1.1rem;line-height:1.8;">{data["translated_text"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"Error: {data.get('detail') or data.get('error')}")


# ── Tab 3: Generate Email ──────────────────────────────
with tab3:
    st.markdown("### Generate Professional Email")
    st.markdown('<p style="color:#94a3b8;font-size:0.9rem;">Describe what you need and get a ready-to-send email.</p>', unsafe_allow_html=True)

    purpose = st.text_area("Purpose of the email *", height=100,
                           placeholder="e.g. Request a meeting to discuss the internship offer and joining date")

    col1, col2 = st.columns(2)
    with col1:
        recipient = st.text_input("Recipient Name", placeholder="HR Manager")
    with col2:
        sender = st.text_input("Your Name", placeholder="Mani Tejeswar Reddy")

    col3, col4 = st.columns(2)
    with col3:
        tone = st.selectbox("Tone", ["professional", "formal", "friendly"])
    with col4:
        context = st.text_input("Additional Context (optional)", placeholder="Any extra details...")

    if st.button("✉️ Generate Email", key="btn_email"):
        if len(purpose.strip()) < 10:
            st.warning("Please describe the purpose (at least 10 characters).")
        else:
            with st.spinner("Writing your email..."):
                status, data = call_api("/generate-email", {
                    "purpose": purpose,
                    "recipient_name": recipient or None,
                    "sender_name": sender or None,
                    "tone": tone,
                    "additional_context": context or None
                })

            if status == 200:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f'**Generated Email** &nbsp; {provider_badge(data["provider"])}', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#94a3b8;margin-top:0.8rem;font-size:0.85rem;">SUBJECT</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#e2e8f0;font-weight:600;">{data["subject"]}</p>', unsafe_allow_html=True)
                st.markdown('<hr style="border-color:rgba(255,255,255,0.08);margin:0.8rem 0;">', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#94a3b8;font-size:0.85rem;">BODY</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color:#e2e8f0;line-height:1.8;white-space:pre-line;">{data["body"]}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Copy button area
                full_email = f"Subject: {data['subject']}\n\n{data['body']}"
                st.text_area("📋 Copy full email", value=full_email, height=200, key="copy_email")
            else:
                st.error(f"Error: {data.get('detail') or data.get('error')}")


# ── Footer ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#475569;font-size:0.8rem;">'
    'Powered by FastAPI + Groq (LLaMA 3.1) | Built by Mani Tejeswar Reddy'
    '</p>',
    unsafe_allow_html=True
)
