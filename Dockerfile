FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=7860 \
    HF_HOME=/tmp/hf_cache \
    TRANSFORMERS_CACHE=/tmp/hf_cache/transformers \
    HF_HUB_CACHE=/tmp/hf_cache/hub \
    XDG_CACHE_HOME=/tmp/hf_cache \
    TORCH_HOME=/tmp/hf_cache/torch \
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

# Force fully ephemeral cache dirs
RUN mkdir -p /tmp/hf_cache && \
    chown -R user:user /tmp/hf_cache

WORKDIR /app

# Install dependencies
COPY --chown=user:user assets/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy app
COPY --chown=user:user . /app

USER user

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]