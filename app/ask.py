from langchain import Llama
import faiss
import json
import os
from app.constants import INDEX_PATH, TEXTS_PATH, CODES
from app.llm import model_path
from app.retrieve import retrieve
from app.build_prompt import build_prompt
from app.faiss_builder import build_index, save_index
from app.chunker import load_data, chunk_documents
from app.response_cleaner import clean_llm_response
from app.get_user_data import response
from app.schemas import ChatRequest


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

    index, texts = load_index()
   
   
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

        temperature=0.1,

        top_p=0.8,

        top_k=20,

        repeat_penalty=1.1,
        
        presence_penalty = 1.5,

        stop=[
         "<|im_end|>",
        "<|im_start|>",
        "</s>",]
    )

    response = output["choices"][0]["text"].strip()

 

    return clean_llm_response(response)




