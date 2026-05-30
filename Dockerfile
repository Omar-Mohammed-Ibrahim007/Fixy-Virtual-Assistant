FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=7860 \
    HF_HOME=/home/user/.cache/huggingface \
    TRANSFORMERS_CACHE=/home/user/.cache/huggingface/transformers \
    HF_HUB_CACHE=/home/user/.cache/huggingface/hub \
    CMAKE_BUILD_PARALLEL_LEVEL=2

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 user

# Create Hugging Face cache directories and give ownership
RUN mkdir -p /home/user/.cache/huggingface && \
    chown -R user:user /home/user/.cache

WORKDIR /app

# Install dependencies first
COPY --chown=user:user assets/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application
COPY --chown=user:user . /app

USER user

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]