from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    answer: str
    citations: str
    sources: List[Dict[str, Any]]

class UploadResponse(BaseModel):
    filename: str
    status: str
    message: str
