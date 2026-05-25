# routes.py

from fastapi import APIRouter
from routes import process_chat
from schemas import (
    ChatRequest,
    ChatResponse
)
from data_cleaner import cleaner_main

router = APIRouter(prefix="/chatbot")

cleaner_main()


@router.post(
    "/support/chatbot",
    response_model=ChatResponse
)
async def chatbot(
    request: ChatRequest
):

    result = await process_chat(
        request.model_dump()
    )

    return result