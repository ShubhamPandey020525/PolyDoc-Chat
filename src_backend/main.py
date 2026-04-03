from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# 1. Professional Path Setup
# Fix for ModuleNotFoundError when running from inside src_backend or root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src_backend.core.config import settings
from src_backend.core.logger import logger
from src_backend.api import upload, chat

# 2. AI Core Global Instances (Shared across API routes)
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from src_ai.services.rag_service import GrokQueryEngine

# Shared instances for dependency injection
hybrid_retriever = HybridRetriever(persist_directory=settings.CHROMA_DB_PATH)
engine = GrokQueryEngine(retriever=hybrid_retriever)

# 3. FastAPI App Initialization
app = FastAPI(
    title="PolyDoc Chat API", 
    version="1.0.0",
    description="Professional Document Intelligence Backend using Grok and RAG"
)

# 4. CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Include Professional API Routes
app.include_router(upload.router, tags=["Ingestion"])
app.include_router(chat.router, tags=["Retrieval-Generation"])

# 6. Global Endpoints
@app.get("/health", tags=["Infrastructure"])
async def health_check():
    return {
        "status": "healthy", 
        "model": settings.GROK_MODEL, 
        "environment": settings.ENVIRONMENT
    }

# 7. Local Run Config
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting professional PolyDoc Backend", 
                host=settings.HOST, 
                port=settings.PORT)
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
