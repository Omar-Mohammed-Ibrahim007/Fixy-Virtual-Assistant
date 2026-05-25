
import time

from app.ask import ask

from schemas import (
    ChatRequest,
    ChatResponse
)


async def process_chat(
    request_data: dict
) -> ChatResponse:

    request = ChatRequest(
        **request_data
    )

    start_time = time.time()

    response = ask(
        request.query
    )

    response_time = round(
        time.time() - start_time,
        2
    )

    return ChatResponse(

        title="Fixy RAG Assistant",

        response_time=response_time,

        code=200,

        description=
        "Response generated successfully",

        response=response
    )