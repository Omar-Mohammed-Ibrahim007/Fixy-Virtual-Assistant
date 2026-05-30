FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=7860 \
    HF_HOME=/data/.cache/huggingface \
    TRANSFORMERS_CACHE=/data/.cache/huggingface/transformers \
    HF_HUB_CACHE=/data/.cache/huggingface/hub

# System deps for python packages that require compilation (keep minimal)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake git && \
    rm -rf /var/lib/apt/lists/*

# Non-root user (recommended for Hugging Face Spaces)
RUN useradd -m -u 1000 user

WORKDIR /app

# Install dependencies first (better caching)
COPY --chown=user:1000 assets/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY --chown=user:1000 . /app

USER user

EXPOSE 7860

# Use the exec form (no shell) for better signal handling
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]

