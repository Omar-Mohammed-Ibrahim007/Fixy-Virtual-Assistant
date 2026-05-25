# Fixy RAG

A retrieval-augmented generation (RAG) assistant built with FastAPI, Faiss, and local LLM integration.

This project processes source documents, extracts question-answer data, builds a vector index, and serves a FastAPI HTTP endpoint so users can query the knowledge base.

## Key Components

- `main.py` - FastAPI application entrypoint with router inclusion.
- `routes.py` - WebSocket chat route handling requests and responses.
- `ask.py` - RAG query workflow: retrieval, prompt construction, and LLM response generation.
- `data_cleaner.py` - Extracts and cleans PDF-based Q&A content.
- `chunker.py` - Loads cleaned data and prepares chunks for vector indexing.
- `faiss_builder.py` - Builds and saves the FAISS index.
- `retrieve.py` - Performs semantic retrieval against the FAISS index.
- `build_prompt.py` / `prompt_builder.py` - Creates prompts for the language model.
- `embeddings.py` - Embedding helper utilities.
- `schemas.py` - Pydantic models for chat request and response payloads.

## Requirements

- Python 3.10+
- `pip install -r assets/requirements.txt`
- Local model files and data assets as referenced in `constants.py`

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r assets/requirements.txt
```

3. Ensure your data and assets are available (paths are defined in `app/constants.py`):

- `Fixy_RAG/data/` should contain `Fixy_RAG_Production_English.pdf`
- `Fixy_RAG/assets/` should contain (or be generated into):
  - `faiss.index`
  - `texts.json`
  - any required model files (see `MODEL_NAME`, `MODEL_REPO`, `MODEL_FILE` in `app/constants.py`)

4. Configure credentials (email):

`app/constants.py` imports credentials from `app/env.py` (module import: `from .env import EMAIL, EMAIL_API_KEY`).

Create `app/env.py`:

```python
EMAIL = "your-email@example.com"
EMAIL_API_KEY = "your-email-api-key"
```

## Running the project

Start the FastAPI app with Uvicorn:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage (chat)

Send a POST request to:

- `POST http://localhost:8000/support/chatbot`

Request body (`ChatRequest`):

```json
{
  "query": "How do I reset my Fixy account password?"
}
```

Response (`ChatResponse`):

```json
{
  "title": "Fixy RAG Assistant",
  "response_time": 0.42,
  "code": 200,
  "description": "Response generated successfully",
  "response": "..."
}
```

## Workflow

1. `data_cleaner.py` extracts text and creates cleaned Q&A data from the input PDF.
2. `chunker.py` converts cleaned items into chunks and builds a FAISS vector index.
3. `ask.py` uses the index and retrieval pipeline to fetch relevant content for a user query.
4. The model generates a response and returns it via the WebSocket chat route.

## Notes

- The current implementation uses local LLM tooling and FAISS for embedding/retrieval (see `app/constants.py` and the RAG pipeline in `app/ask.py`).
- Adjust `app/constants.py` if you need to change dataset paths, model repo names, or index locations.

## License

This repository does not include a license file by default. Add a `LICENSE` as needed for your project.
