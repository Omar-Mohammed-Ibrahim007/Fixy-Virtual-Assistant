
import time
from app.ask import ask
from app.schemas import (
    ChatGetRequest,
    ChatPostRequest,
    ChatResponse
)
from app.get_user_data import get_user_data 
from app.email_service import email_send
from app.state import state
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
async def process_chat(
    request_data: dict# post request data sended by client
) -> ChatResponse:

    get_request =  ChatGetRequest( # get request
    **get_user_data()
    )
    print("Getting close...") 
    post_request=ChatPostRequest(
        **request_data
    )
    start_time = time.time()
    
    index = state.index
    texts = state.texts
    response = ask(
        post_request.query,
        get_request.role,
        get_request.language,
        index,
        texts
    )
    
    print("We almost there..") 
    
   
   
      
    

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
    
 