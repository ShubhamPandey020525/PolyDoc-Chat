import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from src_backend.core.config import settings
from src_backend.core.logger import logger
from src_backend.schemas.api_models import UploadResponse
from src_ai.loaders.document_loaders import LoaderFactory
from langchain_text_splitters import RecursiveCharacterTextSplitter

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    from src_backend.main import hybrid_retriever
    
    if hybrid_retriever is None:
        raise HTTPException(status_code=503, detail="AI Core not initialized. Check API keys in .env")

    upload_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    try:
        # 1. Async File Writing
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: shutil.copyfileobj(file.file, open(upload_path, "wb")))
        
        # 2. Async Loading
        raw_docs = await LoaderFactory.load_async(upload_path)
        
        # 3. Async Strategic Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        chunks = []
        for doc in raw_docs:
            texts = text_splitter.split_text(doc["content"])
            for text in texts:
                chunks.append({"content": text, "metadata": doc["metadata"]})
        
        # 4. Async Indexing
        await hybrid_retriever.add_documents(chunks)
        
        return UploadResponse(
            filename=file.filename,
            status="success",
            message=f"'{file.filename}' indexed successfully."
        )
    except Exception as e:
        logger.error("Upload failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
