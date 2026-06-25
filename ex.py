import google.generativeai as genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel()

