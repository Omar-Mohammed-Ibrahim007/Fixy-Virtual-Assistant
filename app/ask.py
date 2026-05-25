from langchain import Llama
import faiss
import json
import os
from app.constants import INDEX_PATH, TEXTS_PATH, MODEL_PATH
from app.llm import model_path
from app.retrieve import retrieve
from app.build_prompt import build_prompt
from app.faiss_builder import build_index, save_index
from app.chunker import load_data, chunk_documents

llm = Llama( model_path=model_path,
             n_ctx=40960,
             #Maximum context length (tokens)
             n_threads=os.cpu_count(),
             n_gpu_layers=0, # or higher depending on VRAM
             verbose=False,
             #n_batch=512,
             f16_kv=True,)

# =====================================================
# LOAD INDEX
# =====================================================

def load_index():

    index = faiss.read_index(INDEX_PATH)

    with open(
        TEXTS_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        texts = json.load(f)

    return index, texts



# =====================================================
# ASK
# =====================================================

def ask(query):

   
   
   
    # -------------------------------------------------
    # RETRIEVE
    # -------------------------------------------------

    docs = retrieve(
        query,
        index,
        texts
    )

    context = "\n\n".join([

        doc["text"]

        for doc in docs
    ])

    # -------------------------------------------------
    # PROMPT
    # -------------------------------------------------

    prompt = build_prompt(
        query,
        context
    )

    # -------------------------------------------------
    # GENERATE
    # -------------------------------------------------

    output = llm(

        prompt,

        max_tokens=4096,

        temperature=0.3,

        top_p=0.9,

        top_k=40,

        repeat_penalty=1.2,

        stop=[
       "<|im_end|>",
        "<|im_start|>",
        "</s>"]
    )

    response = output["choices"][0]["text"].strip()

 

    return response


# =====================================================
# BUILD INDEX FIRST TIME
# =====================================================

if not os.path.exists(INDEX_PATH):

    print("[+] Building vector database...")

    data = load_data()

    chunks = chunk_documents(data)

    print(f"[+] Total chunks: {len(chunks)}")

    index = build_index(chunks)

    save_index(index, chunks)

    print("[✓] Vector DB Ready")


# =====================================================
# LOAD INDEX
# =====================================================

index, texts = load_index()


