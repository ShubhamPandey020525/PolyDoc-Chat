import asyncio
import os
import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from src_backend.core.config import settings
from src_backend.core.logger import logger
from src_backend.schemas.api_models import UploadResponse, MultiUploadResponse
from src_ai.loaders.document_loaders import LoaderFactory
from langchain_text_splitters import RecursiveCharacterTextSplitter

router = APIRouter()

# One splitter instance
_TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
)

def _save_upload_to_disk(source, dest_path: str) -> None:
    with open(dest_path, "wb") as out:
        shutil.copyfileobj(source, out)

def _chunk_single_doc(doc: dict) -> list:
    chunks = _TEXT_SPLITTER.split_text(doc["content"])
    return [{"content": c, "metadata": doc["metadata"]} for c in chunks]

@router.post("/upload", response_model=MultiUploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    from src_backend.core import state

    if state.retriever is None:
        logger.error("Upload failed: AI Core not initialized")
        raise HTTPException(
            status_code=503, 
            detail="AI Core not initialized. Please ensure GROQ_API_KEY is set in your .env file."
        )

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    results = []
    all_chunks = []
    loop = asyncio.get_event_loop()

    for file in files:
        upload_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        try:
            await file.seek(0)
            await loop.run_in_executor(None, _save_upload_to_disk, file.file, upload_path)

            raw_docs = await LoaderFactory.load_async(upload_path)
            
            chunk_tasks = [loop.run_in_executor(None, _chunk_single_doc, doc) for doc in raw_docs]
            chunk_results = await asyncio.gather(*chunk_tasks)
            doc_chunks = [item for sublist in chunk_results for item in sublist]
            all_chunks.extend(doc_chunks)

            results.append(UploadResponse(
                filename=file.filename,
                status="success",
                message=f"'{file.filename}' processed successfully."
            ))
        except Exception as e:
            logger.error(f"Upload failed for {file.filename}", error=str(e))
            results.append(UploadResponse(
                filename=file.filename,
                status="error",
                message=str(e)
            ))

    if all_chunks:
        await state.retriever.add_documents(all_chunks)
    
    return MultiUploadResponse(files=results)

@router.delete("/clear", response_model=dict)
async def clear_knowledge_base():
    from src_backend.core import state
    if state.retriever is None:
        raise HTTPException(status_code=503, detail="AI Core not initialized")
    
    try:
        # Delete all documents from Chroma
        state.retriever.db.delete_collection()
        # Re-initialize to create a fresh collection
        state.retriever.db = state.retriever._init_db()
        
        # Clear uploads folder
        if os.path.exists(settings.UPLOAD_DIR):
            shutil.rmtree(settings.UPLOAD_DIR)
            os.makedirs(settings.UPLOAD_DIR)
            
        return {"status": "success", "message": "Knowledge base cleared successfully."}
    except Exception as e:
        logger.error("Failed to clear knowledge base", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
