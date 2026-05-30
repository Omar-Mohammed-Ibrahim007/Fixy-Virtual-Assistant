
import time
from app.ask import ask
from app.response_cleaner import clean_llm_response
from app.schemas import (
    ChatGetRequest,
    ChatPostRequest,
    ChatResponse
)
from app.get_user_data import get_user_data 
from app.email_service import email_send

async def process_chat(
    request_data: dict # post request data sended by client
) -> ChatResponse:

    get_request = await ChatGetRequest( # get request
    **get_user_data()
    )
    post_request=ChatPostRequest(
        **request_data
    )
    start_time = time.time()

    response = ask(
        post_request.query,
        get_request.role,
        get_request.language
    )
    
    response=clean_llm_response(response)
   
    
    

    response_time = round(
        time.time() - start_time,
        2
    )
     
    if response.get("needs_support", False):
        email_send(
            get_request.language,
            response.get("title", "null"),
            response.get("code", "null"),
            get_request.userID,
            get_request.role,
            get_request.email,
            response.get("name","null" ),
            post_request.query,
            response_time
        )

    return ChatResponse(

        title=response.get("title","no title"),
        
        section=response.get("section", "General"),

        response_time=response_time,

        code=response.get("code", 0),
        
        name=response.get("code_title")['name'] if response.get("code_title") else "Unknown",

        description=response.get("code_title")['description']if response.get("code_title") else "Unknown",

        response=response.get("response", "No response"),   
        
        escalate_to_support=response.get("needs_support", False),
        
        source=response.get("source", "Unknown"),
        
    )
    
 