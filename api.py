import time

from ask import ask

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

    # TIMER START
    start_time = time.time()

    # RAG FUNCTION
    response = ask(
        request.query
    )

    # TIMER END
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