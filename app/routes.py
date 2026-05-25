# routes.py

from fastapi import APIRouter
from schemas import (
    ChatRequest,
    ChatResponse
)
from app.api import process_chat

router = APIRouter()


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