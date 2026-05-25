from embeddings import embeddings_model
import numpy as np

def retrieve(query, index, texts, k=5):

    MIN_SCORE = 0.45

    # ---------------- QUERY EMBEDDING ----------------
    formatted_query = f"query: {query}"

    q_emb = embeddings_model.embed_documents([formatted_query])
    q_emb = np.array(q_emb, dtype=np.float32)

    # ---------------- FAISS SEARCH ----------------
    scores, indices = index.search(q_emb, k)

    results = []
    seen = set()

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        if score < MIN_SCORE:
            continue

        if idx >= len(texts):
            continue

        chunk = texts[idx]
        text = chunk["text"]

        if text in seen:
            continue

        seen.add(text)

        results.append({
            "score": float(score),
            "text": text,
            "metadata": chunk.get("metadata", {})
        })

    return results