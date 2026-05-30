from app.constants import Assets_dir
import json
from app.faiss_builder import build_index, save



# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    with open(
        f"{Assets_dir}/rag_english_data_cleaned.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# =====================================================
# CHUNKING
# =====================================================
def chunk_documents(data):

    all_chunks = []

    for i, item in enumerate(data):

        context = item["context"]

        all_chunks.append({

            "text": context,  # FULL content, no splitting

            "metadata": {

                "chunk_id": i,  # now unique per document (not per split)

                "source": item.get("source", "unknown"),

                "title": item.get("title", "unknown"),

                "qa_id": item.get("QA_ID", "unknown")
            }
        })

    return all_chunks


    

# =====================================================
# MAIN
# =====================================================
def chunker_main():
  
    print("[+] Loading data...")

    data = load_data()

    print("[+] Chunking documents...")

    chunks = chunk_documents(data)

    print(f"[+] Total chunks: {len(chunks)}")

    index = build_index(chunks)

    save(index, chunks)

