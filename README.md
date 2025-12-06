## 1. Setup Environment relative to the `essays/sentiment/backend` folder:
I have already created a virtual environment for you.

```bash
# If you need to re-create it:
python3 -m venv venv
./venv/bin/pip install fastapi uvicorn google-generativeai python-multipart python-dotenv
```

## 2. API Key
Ensure you have a `.env` file in this directory with your Gemini API key:
```
GEMINI_API_KEY=AIzaSy...
```

## 3. Run the Satellite Server
Run this command in your terminal to start the backend using the environment:
```bash
./venv/bin/python server.py
```
*You should see output indicating the server is running on `http://127.0.0.1:8000`.*

## 4. Launch the Lab
1. Go to your browser and open the main **Sentiment Explorer** (`index.html`).
2. Select some chat messages.
3. Click **INITIALIZE LAB TRANSFER**.
4. The system will send data to your running local server and open the Lab interface.
