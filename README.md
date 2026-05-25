# Fixy RAG

A retrieval-augmented generation (RAG) assistant built with FastAPI, Faiss, and local LLM integration.

This project processes source documents, extracts question-answer data, builds a vector index, and serves a WebSocket chat endpoint so users can query the knowledge base.

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

3. Ensure your data and assets are available:

- `data/` should contain the source PDF data files.
- `assets/` should contain the cleaned JSON, index files, and any model files required.

4. Configure credentials:

The project references `EMAIL` and `EMAIL_API_KEY` values from a local `env.py` or environment configuration. Create `env.py` if needed:

```python
EMAIL = "your-email@example.com"
EMAIL_API_KEY = "your-email-api-key"
```

## Running the project

Start the FastAPI app with Uvicorn:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### REST API

- **Health Check**: `GET http://localhost:8000/health`
- **Chat Query**: `POST http://localhost:8000/api/chat`
  - Request body: `{"query": "your question here"}`
- **System Info**: `GET http://localhost:8000/api/info`
- **API Docs**: `GET http://localhost:8000/docs` (Swagger UI)

## Deployment

### Hugging Face Spaces

Deploy your RAG application to Hugging Face Spaces using Docker:

1. Push your repository to GitHub
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new Space
3. Select **Docker** as the space type
4. Connect your GitHub repository
5. Hugging Face will automatically build and deploy using the included Dockerfile

The application will be accessible at: `https://<your-username>-<space-name>.hf.space`

**Note:** The Dockerfile is configured to run on port 7860 (required by Hugging Face Spaces).

## Workflow

1. `data_cleaner.py` extracts text and creates cleaned Q&A data from the input PDF.
2. `chunker.py` converts cleaned items into chunks and builds a FAISS vector index.
3. `ask.py` uses the index and retrieval pipeline to fetch relevant content for a user query.
4. The model generates a response and returns it via the WebSocket chat route.

## Notes

- The current implementation uses local LLM tooling and FAISS for on-device embedding/retrieval.
- Adjust `constants.py` if you need to change dataset paths, model repo names, or index locations.
- If the WebSocket server import path needs updating, ensure `main.py` and `routes.py` are aligned with your module layout.

## License

This repository does not include a license file by default. Add a `LICENSE` as needed for your project.
