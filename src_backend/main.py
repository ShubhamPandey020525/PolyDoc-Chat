import os
import sys

# --- PROFESSIONAL PATH FIX (MUST BE AT THE VERY TOP) ---
# Ye line ensure karti hai ki 'src_ai' aur 'src_backend' dono mil jayein
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# -------------------------------------------------------

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from src_backend.core.config import settings
from src_backend.core.logger import logger
from src_backend.api import upload, chat
from src_backend.core import state

# AI Core Global Instances
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from src_ai.services.rag_service import GrokQueryEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async startup/shutdown; keeps event loop responsive (no blocking in startup)."""
    logger.info("PolyDoc API lifespan: initializing AI core")
    try:
        state.hybrid_retriever = HybridRetriever(persist_directory=settings.CHROMA_DB_PATH)
        state.engine = GrokQueryEngine(retriever=state.hybrid_retriever)
    except Exception as e:
        logger.error("AI Core initialization failed (Check .env keys later)", error=str(e))
        state.hybrid_retriever = None
        state.engine = None
    yield
    logger.info("PolyDoc API lifespan: shutdown complete")


app = FastAPI(
    title="PolyDoc Chat API",
    version="1.0.0",
    description="Professional Document Intelligence Backend",
    lifespan=lifespan,
)

# Async Performance Monitoring Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request {request.url.path} processed in {process_time:.4f}s")
    return response

# Professional CORS & Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
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
