import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: Could not find GEMINI_API_KEY in .env file")
    exit()

genai.configure(api_key=api_key)

print(f"Checking available models for your API key...")
print("-" * 40)

try:
    # List all models available to your key
    for m in genai.list_models():
        # Only show models that can generate text (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
            
except Exception as e:
    print(f"❌ Error connecting to Google: {e}")