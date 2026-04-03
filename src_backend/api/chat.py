from fastapi import APIRouter, HTTPException
from src_backend.core.logger import logger
from src_backend.schemas.api_models import ChatRequest, ChatResponse
from src_ai.services.rag_service import GrokQueryEngine

router = APIRouter()

# Share the engine instance globally in main.py
def get_engine():
    from src_backend.main import engine
    return engine

@router.post("/chat", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """Processes a user query through the Grok-powered RAG pipeline."""
    try:
        engine = get_engine()
        result = engine.process(
            query=request.query, 
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            answer=result["answer"],
            citations=result["citations"],
            sources=result["sources"]
        )
        
    except Exception as e:
        logger.error("Chat query failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
