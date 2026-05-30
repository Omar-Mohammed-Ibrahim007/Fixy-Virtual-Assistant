# routes.py
from fastapi import  FastAPI
from app.data_cleaner import cleaner_main
from app.routes import router
from app.chunker import chunker_main
from contextlib import asynccontextmanager
from fastapi import FastAPI
import app.state as state
from app.api import load_index
@asynccontextmanager # run these functions only at startupno every reload
async def lifespan(app: FastAPI):
    cleaner_main()
    chunker_main()
    state.index, state.texts = load_index()
    print("✅ FAISS index loaded once at startup")
    
    yield
    
app = FastAPI(lifespan=lifespan)


app.include_router(router)

