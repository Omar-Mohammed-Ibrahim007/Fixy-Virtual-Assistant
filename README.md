---
title: Fixy Virtual Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app/main.py
pinned: false
---
# Fixy RAG

A retrieval-augmented generation (RAG) assistant built with FastAPI, Faiss, and local LLM integration.

This project processes source documents, extracts question-answer data, builds a vector index, and serves a FastAPI HTTP endpoint so users can query the knowledge base.

For Hugging Face Spaces/Docker, see `assets/Dockerfile` (port 7860 + Hugging Face cache environment variables).


## Key Components

- `app/main.py` - FastAPI application entrypoint. Runs `cleaner_main()` and `chunker_main()` at startup (lifespan hook).
- `app/routes.py` - HTTP endpoint for the assistant:
  - `POST /support/Fixy_AI_assistant`
- `app/api.py` - Request handling. Builds a `ChatRequest` from `app/get_user_data.py` and runs the RAG pipeline.
- `app/ask.py` - Core RAG workflow: loads FAISS index, retrieves relevant context, builds the prompt, generates with the local LLM, and cleans the output.
- `app/data_cleaner.py` - Extracts and cleans PDF-based Q&A content.
- `app/chunker.py` - Loads cleaned data and prepares it for vector indexing.
- `app/faiss_builder.py` - Builds and saves the FAISS index.
- `app/retrieve.py` - Performs semantic retrieval against the FAISS index.
- `app/build_prompt.py` - Creates prompts for the language model.
- `app/schemas.py` - Pydantic models for chat request and response payloads.

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

- `Fixy_RAG/data/` should contain:
  - `Fixy_RAG_Production_English.pdf`
- `Fixy_RAG/assets/` should contain (or be generated into):
  - `faiss.index` (used for retrieval)
  - `texts.json` (used alongside the FAISS index)

4. Email credentials (used when `needs_support=true`):

`app/constants.py` reads these from environment variables (via `app/env.py` / `.env` using `dotenv`):

- `RECIEVER_EMAIL`
- `RECIEVER_EMAIL_API_KEY`
- `SENDER_EMAIL`
- `SENDER_EMAIL_API_KEY`

## Running the project

Start the FastAPI app with Uvicorn (default port 8000 for local dev):

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker / Hugging Face Spaces

The provided `assets/Dockerfile` is configured for:

- Port: `7860`
- Host binding: `0.0.0.0`
- Hugging Face cache envs:
  - `HF_HOME`
  - `TRANSFORMERS_CACHE`
  - `HF_HUB_CACHE`

Build/run instructions are documented in `assets/Dockerfile` behavior (see `CMD ... --port ${PORT}`).

## API Usage (support assistant)

This service exposes a single HTTP POST endpoint:

- `POST http://localhost:8000/support/Fixy_AI_assistant`

> Important: `app/api.py` ignores/overrides the client payload and constructs the `ChatRequest` using `app/get_user_data.py` (it fetches/returns user context; it falls back to a sample payload on error).


Request body (`ChatRequest`):

Because the server builds `ChatRequest` using `app/get_user_data.py`, your client payload may not be used as-is. Still, the `ChatRequest` model fields are:

```json
{
  "query": "How do I reset my Fixy account password?",
  "email": "example@gmail.com",
  "role": "user",
  "userID": 123,
  "username": "some-user",
  "language": "en"
}
```

Response (`ChatResponse`):

```json
{
  "title": "Fixy RAG Assistant",
  "section": "General",
  "response_time": 0.42,
  "code": 200,
  "name": "answer_found",
  "description": "Answer exists in context or reliable knowledge",
  "response": "...",
  "escalate_to_support": false,
  "source": "Unknown"
}
```

## Workflow

On server startup (`app/main.py` lifespan hook):

1. `app/data_cleaner.py` extracts and cleans the PDF content.
2. `app/chunker.py` prepares cleaned items for indexing.

At request time (`POST /support/Fixy_AI_assistant`):

1. `app/api.py` builds a `ChatRequest` using `app/get_user_data.py`.
2. `app/ask.py`:
   - loads `faiss.index` + `texts.json`
   - retrieves relevant documents (`app/retrieve.py`)
   - builds a prompt (`app/build_prompt.py`)
   - generates using the local LLM (`app/llm.py` via LangChain Llama)
   - cleans the output (`app/response_cleaner.py`)
3. If `needs_support=true`, `app/email.py` sends an escalation email.

## Notes

- Retrieval uses FAISS with embeddings configured in `app/embeddings.py` (configured via `app/constants.py` for model/index paths).
- Generation uses a local LLM (see `app/llm.py` and `app/ask.py` for inference parameters).
- Adjust `app/constants.py` if you need to change dataset paths, model repo/file names, or index/data locations.

## License

This repository does not include a license file by default. Add a `LICENSE` as needed for your project.
