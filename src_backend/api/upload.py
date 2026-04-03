from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from src_backend.core.config import settings
from src_backend.core.logger import logger
from src_backend.schemas.api_models import UploadResponse
from src_ai.loaders.document_loaders import LoaderFactory
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

router = APIRouter()

# Share the retriever instance globally in main.py
def get_retriever():
    from src_backend.main import hybrid_retriever
    return hybrid_retriever

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Handles file uploads and indexes them into the AI Core."""
    upload_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    try:
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info("File uploaded", filename=file.filename)
        
        # 1. Load Document
        raw_docs = LoaderFactory.load(upload_path)
        
        # 2. Strategic Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        
        chunks = []
        for doc in raw_docs:
            texts = text_splitter.split_text(doc["content"])
            for text in texts:
                chunks.append({
                    "content": text,
                    "metadata": doc["metadata"]
                })
        
        # 3. Indexing
        retriever = get_retriever()
        retriever.add_documents(chunks)
        
        return UploadResponse(
            filename=file.filename,
            status="success",
            message=f"Document '{file.filename}' processed and indexed successfully."
        )
        
    except Exception as e:
        logger.error("Upload/Indexing failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
