# routes.py
from fastapi import  FastAPI
from app.data_cleaner import cleaner_main
from app.routes import router
from app.chunker import chunker_main
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.constants import INDEX_PATH,TEXTS_PATH
import json
import faiss
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


@asynccontextmanager # run these functions only at startupno every reload
async def lifespan(app: FastAPI):
    cleaner_main()
    chunker_main()
    yield
    
index, texts = load_index()

app = FastAPI(lifespan=lifespan)


app.include_router(router)

