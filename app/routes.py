# routes.py

from fastapi import APIRouter
from app.schemas import (
    ChatGetRequest,
    ChatPostRequest,
    ChatResponse
)
from app.api import process_chat
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

index, texts = load_index()

# =====================================================
router = APIRouter(tags=["virtual_assistant"])


@router.post(
    "/support/Fixy_AI_assistant",
    response_model=ChatResponse
)
async def chatbot(
    request: ChatPostRequest 
):

    result = await process_chat(
        request.model_dump(),
        index,
        texts
    )

    return result 