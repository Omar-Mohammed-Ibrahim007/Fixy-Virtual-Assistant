from pydantic import BaseModel
from typing import Optional


# ==========================================
# REQUEST MODEL
# ==========================================
class ChatPostRequest(BaseModel):
    query: str
    
    
class ChatGetRequest(BaseModel):
    email: str
    role: str
    userID: int
    username: str
    language: Optional[str] = "en"
    


# ==========================================
# RESPONSE MODEL
# ==========================================

class ChatResponse(BaseModel):

    title: str
    
    section: str

    response_time: float

    code: int
    
    name: str

    description: str

    response: str
    
    escalate_to_support: bool
    
    source: str
    