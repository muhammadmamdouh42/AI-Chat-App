## Overview
The backend provides the server-side API via FastAPI. It includes document ingestion, a vectorstore handler, and a LangGraph agent.

### Endpoints
- `POST /upload`: Upload and persist documents, then ingest into the vectorstore.
- `POST /ask`: Accept a user prompt and return an AI-generated response via the agent.

## Setup & Run
1. **Environment Variables**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `backend/.env` and set:
     ```ini
     OPENAI_API_KEY="sk-..."
     TAVILY_API_KEY="tvly-..."
     # (optional) OPENAI_MODEL="openai:gpt-4o-mini"
     ```
2. **Python Virtual Environment**
   - Create and activate a venv:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Server**
   ```bash
   uvicorn app.main:fastapi_app --reload --host 0.0.0.0 --port 8000
   ```
## Testing the Backend
- Upload file:
  ```bash
  curl -F "files=@/path/to/doc.pdf" http://localhost:8000/upload
  ```
- Submit a question:
  ```bash
  curl -H "Content-Type: application/json" \
       -d '{"prompt":"Your question here"}' \
       http://localhost:8000/ask
  ```
