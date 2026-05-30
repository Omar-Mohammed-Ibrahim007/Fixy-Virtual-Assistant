from huggingface_hub import hf_hub_download
from app.constants import MODEL_REPO, MODEL_FILE

model_path = hf_hub_download(
    repo_id="Qwen/Qwen3-4B-GGUF",
    filename="Qwen3-4B-Q8_0.gguf",
    force_download=True,
    resume_download=False
)