FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV PORT=7860

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential cmake git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY assets/requirements.txt ./assets/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r assets/requirements.txt \
    fastapi uvicorn[standard] transformers torch faiss-cpu langchain langchain-community huggingface-hub pdfminer.six llama-cpp-python numpy requests pydantic zstandard

COPY . /app

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
