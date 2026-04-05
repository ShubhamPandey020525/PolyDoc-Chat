from fastapi import APIRouter, HTTPException
from src_backend.core.logger import logger
from src_backend.schemas.api_models import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    from src_backend.core import state
    
    if state.engine is None:
        raise HTTPException(status_code=503, detail="AI Engine not initialized. Check API keys in .env")

    try:
        # Now calling async process
        result = await state.engine.process(
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
