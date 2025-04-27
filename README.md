## Setup Instructions

For detailed environment setup and dependencies, please refer to the service-specific README files:

- [Backend Setup](backend/README.md)
- [Frontend Setup](frontend/README.md)

## Running the Application
You can run both backend and frontend locally for development:

- **Backend** (on port 8000):
  ```bash
  cd backend
  uvicorn app.main:fastapi_app --reload --host 0.0.0.0 --port 8000
  ```
  This will launch the FastAPI server and auto-reload on code changes.

- **Frontend** (on port 5173):
  ```bash
  cd frontend
  npm run dev
  ```
  You can then access the UI at `http://localhost:5173` in your browser.

## Testing the Application

### Uploading Documents
- **Via UI**: Use the Upload section in the interface to submit `.pdf` or `.txt` files.
- **Via curl**:
  ```bash
  curl -F "files=@/path/to/doc.pdf" http://localhost:8000/upload
  ```
  You can upload multiple files in one request.

### Asking Questions
- **Via UI**: Enter your prompt into the input box and click the **Send** button.
- **Via curl**:
  ```bash
  curl -H "Content-Type: application/json" \
       -d '{"prompt":"Your question here"}' \
       http://localhost:8000/ask
  ```
  A JSON response will return with the AI's answer.

## RAG + Agent Architecture
This application combines Retrieval-Augmented Generation (RAG) with an intelligent LangGraph-based ReAct agent.

- **RAG Flow**: Uploaded documents are chunked into manageable parts, then embedded using OpenAIEmbeddings and stored in a Chroma vectorstore. When a user submits a question, the system retrieves contextually relevant chunks to guide the AI's response.

- **ReAct Agent**: The core engine is a LangGraph-powered ReAct agent. It enhances responses using tools such as:
  - A secure calculator for evaluating expressions.
  - A UTC date-fetching utility for getting today's date.
  - A document retriever tool to search within uploaded files.
  - Tavily web search integration for real-time results.

  The agent also uses an in-memory thread-based context to retain lightweight history across interactions.
