import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=api_key)

app = FastAPI()

# Enable CORS
# In production, set ALLOWED_ORIGINS="https://your-portfolio.github.io" in Render environment variables
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Storage for the latest transfer
# This acts as a bridge between the "Explorer" (static site) and the "Lab" (this backend)
LAB_CONTEXT = {
    "data": [],
    "meta": "No data transferred yet."
}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve the Lab UI
    with open("lab.html", "r") as f:
        return f.read()

@app.post("/transfer")
async def transfer_data(payload: dict):
    """Receives selected logs from the static site."""
    global LAB_CONTEXT
    LAB_CONTEXT["data"] = payload.get("data", [])
    LAB_CONTEXT["meta"] = payload.get("meta", {})
    return {"status": "success", "count": len(LAB_CONTEXT["data"])}

@app.get("/context")
async def get_context():
    """Returns the current stored data to the Lab UI."""
    return LAB_CONTEXT

@app.post("/analyze")
async def analyze_sentiment(request: Request):
    """Sends prompt + data to Gemini."""
    body = await request.json()
    prompt = body.get("prompt", "")
    data_sample = body.get("data", [])

    if not api_key:
        return JSONResponse(status_code=500, content={"error": "API Key Missing"})

    try:
        # Confirmed Model: Gemini 2.5 Pro
        model = genai.GenerativeModel('models/gemini-2.5-pro') 
        
        # Construct the context prompt
        full_prompt = f"""
        You are an advanced Sentiment Analysis AI functioning within a 'Sentiment Lab'.
        
        ANALYSIS TASK:
        {prompt}

        DATASET ({len(data_sample)} messages):
        {str(data_sample)}
        
        Provide a concise, technical analysis. Use JSON format if requested.
        """
        
        response = model.generate_content(full_prompt)
        return {"response": response.text}
        
    except Exception as e:
        # Log the full error to the terminal so the user can see it
        print(f"CRITICAL ERROR IN /analyze: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
