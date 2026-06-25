import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say hello in one sentence."}]
    )
    print("[OK] Groq Working!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("[FAIL] Groq Failed:", str(e)[:200])
