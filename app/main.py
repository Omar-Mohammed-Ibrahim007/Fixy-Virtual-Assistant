# routes.py
from fastapi import APIRouter, FastAPI
from app.data_cleaner import cleaner_main
from app.ask import ask
from app.routes import router
from app.chunker import chunker_main
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager # run these functions only at startupno every reload
async def lifespan(app: FastAPI):
    cleaner_main()
    chunker_main()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(router)

