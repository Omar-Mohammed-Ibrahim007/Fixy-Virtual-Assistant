
import time
from app.ask import ask
from app.response_cleaner import clean_llm_response
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
    
    response=clean_llm_response(response)

    response_time = round(
        time.time() - start_time,
        2
    )

    return ChatResponse(

        title=response.get("title","no title"),
        
        section=response.get("section", "General"),

        response_time=response_time,

        code=response.get("code", 0),
        
        name=response.get("code_title")['name'] if response.get("code_title") else "Unknown",

        description=response.get("code_title")['description']if response.get("code_title") else "Unknown",

        response=response.get("response", "No response")    
        
        escalate_to_support=response.get("needs_support", False),
        
        source=response.get("source", "Unknown"),
        
    )
    
 