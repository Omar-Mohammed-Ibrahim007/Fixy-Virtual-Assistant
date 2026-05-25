from pydantic import BaseModel
from typing import Optional


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):

    query: str


# ==========================================
# RESPONSE MODEL
# ==========================================

class ChatResponse(BaseModel):

    title: str

    response_time: float

    code: int

    description: str

    response: str