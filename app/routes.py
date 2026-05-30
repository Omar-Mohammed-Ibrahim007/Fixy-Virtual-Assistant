# routes.py

from fastapi import APIRouter
from app.schemas import (
    ChatGetRequest,
    ChatPostRequest,
    ChatResponse
)
from app.api import process_chat

router = APIRouter(tags=["virtual_assistant"])


@router.post(
    "/support/Fixy_AI_assistant",
    response_model=ChatResponse
)
async def chatbot(
    request: ChatPostRequest 
):

    result = await process_chat(
        request.model_dump()
    )

    return result 