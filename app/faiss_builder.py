import json
import faiss
from app.constants import  INDEX_PATH, TEXTS_PATH
import numpy as np
from app.embeddings import embeddings_model
def build_index(chunks):

  

    texts = [
        f"passage: {chunk['text']}"
        for chunk in chunks
    ]

    print("[+] Creating embeddings...")

    embeddings = embeddings_model.embed_documents(texts)

    embeddings = np.array(embeddings, dtype=np.float32)

    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    return index
# =====================================================
# SAVE
# =====================================================

def save(index, chunks):

    faiss.write_index(index, INDEX_PATH)

    with open(
        TEXTS_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("[✓] Index saved successfully")

