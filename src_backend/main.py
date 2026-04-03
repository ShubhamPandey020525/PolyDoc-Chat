import os
import sys

# --- PROFESSIONAL PATH FIX (MUST BE AT THE VERY TOP) ---
# Ye line ensure karti hai ki 'src_ai' aur 'src_backend' dono mil jayein
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# -------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src_backend.core.config import settings
from src_backend.core.logger import logger
from src_backend.api import upload, chat

# AI Core Global Instances
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from src_ai.services.rag_service import GrokQueryEngine

# Initialize shared instances
# Note: Ye tabhi chalenge jab .env me keys hongi, par error nahi denge start hone par
try:
    hybrid_retriever = HybridRetriever(persist_directory=settings.CHROMA_DB_PATH)
    engine = GrokQueryEngine(retriever=hybrid_retriever)
except Exception as e:
    logger.error("AI Core initialization failed (Check .env keys later)", error=str(e))
    hybrid_retriever = None
    engine = None

app = FastAPI(
    title="PolyDoc Chat API", 
    version="1.0.0",
    description="Professional Document Intelligence Backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, tags=["Ingestion"])
app.include_router(chat.router, tags=["Retrieval-Generation"])

@app.get("/health", tags=["Infrastructure"])
async def health_check():
    return {
        "status": "healthy", 
        "api_keys_set": bool(settings.XAI_API_KEY and settings.OPENAI_API_KEY),
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
