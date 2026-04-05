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

# One splitter instance: same config for all docs on this request (faster than rebuilding per doc)
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


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    from src_backend.main import hybrid_retriever

    if hybrid_retriever is None:
        logger.error("Upload failed: AI Core not initialized")
        raise HTTPException(
            status_code=503, 
            detail="AI Core not initialized. Please ensure XAI_API_KEY and OPENAI_API_KEY are set in your .env file."
        )

    upload_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    try:
        await file.seek(0)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _save_upload_to_disk, file.file, upload_path)

        raw_docs = await LoaderFactory.load_async(upload_path)

        chunk_tasks = [loop.run_in_executor(None, _chunk_single_doc, doc) for doc in raw_docs]
        chunk_results = await asyncio.gather(*chunk_tasks)
        chunks = [item for sublist in chunk_results for item in sublist]

        await hybrid_retriever.add_documents(chunks)
        
        return UploadResponse(
            filename=file.filename,
            status="success",
            message=f"'{file.filename}' indexed successfully."
        )
    except Exception as e:
        logger.error("Upload failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
