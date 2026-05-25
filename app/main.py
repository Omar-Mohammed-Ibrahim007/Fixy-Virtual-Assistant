# routes.py
from fastapi import APIRouter, FastAPI
from app.routes import process_chat
from app.data_cleaner import cleaner_main
from app.ask import ask
from routes import router

app = FastAPI()

app.include_router(router)

