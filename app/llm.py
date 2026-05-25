from huggingface_hub import hf_hub_download
from app.constants import MODEL_REPO, MODEL_FILE


model_path = hf_hub_download(
    repo_id=MODEL_REPO,
    filename=MODEL_FILE,
    cache_dir="./Fixy_RAG/RAG/"
)

print(model_path)