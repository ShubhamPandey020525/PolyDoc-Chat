import fitz  # PyMuPDF
import pandas as pd
from docx import Document
from typing import List, Dict, Any
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from src_ai.core.logger import logger


def _pdf_extract_page(page_num: int, doc_path: str) -> Dict[str, Any]:
    """One page per thread; each thread opens its own document (PyMuPDF is not thread-safe on one doc)."""
    doc = fitz.open(doc_path)
    try:
        page = doc[page_num]
        text = page.get_text()
    finally:
        doc.close()
    return {
        "content": text,
        "metadata": {
            "source": os.path.basename(doc_path),
            "page_number": page_num + 1,
            "file_type": "pdf",
        },
    }


def _load_pdf_pages_threaded(file_path: str) -> List[Dict[str, Any]]:
    """CPU/IO-bound PDF text extraction parallelized with ThreadPoolExecutor."""
    doc = fitz.open(file_path)
    try:
        num_pages = len(doc)
    finally:
        doc.close()

    if num_pages == 0:
        return []

    cpu = os.cpu_count() or 4
    max_workers = min(32, num_pages, max(4, cpu * 2))

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        # map preserves input order → page order stays correct
        return list(pool.map(_pdf_extract_page, range(num_pages), [file_path] * num_pages))


class DocumentLoader:
    """Consolidated document loader for all professional file types with Parallel Processing."""

    @staticmethod
    async def load_pdf_async(file_path: str) -> List[Dict[str, Any]]:
        """Loads PDF pages in parallel via ThreadPoolExecutor (non-blocking to asyncio event loop)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _load_pdf_pages_threaded, file_path)

    @staticmethod
    async def load_table_async(file_path: str) -> List[Dict[str, Any]]:
        """Loads CSV/Excel in an async-friendly way."""
        loop = asyncio.get_event_loop()
        
        def _read_table():
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            rows = []
            for index, row in df.iterrows():
                rows.append({
                    "content": row.to_string(),
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "row_index": index,
                        "file_type": "table"
                    }
                })
            return rows

        return await loop.run_in_executor(None, _read_table)

    @staticmethod
    async def load_docx_async(file_path: str) -> List[Dict[str, Any]]:
        """Loads DOCX in an async-friendly way."""
        loop = asyncio.get_event_loop()
        
        def _read_docx():
            doc = Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            
            return [{
                "content": "\n".join(full_text),
                "metadata": {
                    "source": os.path.basename(file_path),
                    "file_type": "docx"
                }
            }]

        return await loop.run_in_executor(None, _read_docx)

    @staticmethod
    async def load_txt_async(file_path: str) -> List[Dict[str, Any]]:
        """Loads TXT in an async-friendly way."""
        loop = asyncio.get_event_loop()
        
        def _read_txt():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return [{
                "content": content,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "file_type": "txt"
                }
            }]

        return await loop.run_in_executor(None, _read_txt)

class LoaderFactory:
    """Professional Factory to handle multi-format document ingestion asynchronously."""
    
    @staticmethod
    async def load_async(file_path: str) -> List[Dict[str, Any]]:
        ext = os.path.splitext(file_path)[1].lower()
        logger.info(f"Asynchronously loading {ext} file: {file_path}")
        
        if ext == '.pdf':
            return await DocumentLoader.load_pdf_async(file_path)
        elif ext in ['.csv', '.xlsx', '.xls']:
            return await DocumentLoader.load_table_async(file_path)
        elif ext == '.docx':
            return await DocumentLoader.load_docx_async(file_path)
        elif ext == '.txt':
            return await DocumentLoader.load_txt_async(file_path)
        else:
            logger.error(f"Unsupported file type: {ext}")
            raise ValueError(f"Unsupported file type: {ext}")
