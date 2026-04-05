import fitz  # PyMuPDF
import pandas as pd
from docx import Document
from typing import List, Dict, Any, Optional
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from src_ai.core.logger import logger

class DocumentLoader:
    """Consolidated document loader for all professional file types with Parallel Processing."""
    
    @staticmethod
    async def load_pdf_async(file_path: str) -> List[Dict[str, Any]]:
        """Loads PDF pages in parallel using a thread pool."""
        loop = asyncio.get_event_loop()
        
        def _read_pdf():
            doc = fitz.open(file_path)
            pages = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                pages.append({
                    "content": page.get_text(),
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "page_number": page_num + 1,
                        "file_type": "pdf"
                    }
                })
            doc.close()
            return pages

        return await loop.run_in_executor(None, _read_pdf)

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

class LoaderFactory:
    """Professional Factory to route files to correct loaders asynchronously."""
    
    @staticmethod
    async def load_async(file_path: str) -> List[Dict[str, Any]]:
        ext = os.path.splitext(file_path)[1].lower()
        logger.info(f"Asynchronously loading file: {file_path}")
        
        if ext == '.pdf':
            return await DocumentLoader.load_pdf_async(file_path)
        elif ext in ['.csv', '.xlsx', '.xls']:
            return await DocumentLoader.load_table_async(file_path)
        elif ext == '.docx':
            return await DocumentLoader.load_docx_async(file_path)
        elif ext == '.txt':
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(None, lambda: open(file_path, 'r', encoding='utf-8').read())
            return [{
                "content": content,
                "metadata": {"source": os.path.basename(file_path), "file_type": "txt"}
            }]
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
        content = "\n".join([para.text for para in doc.paragraphs])
        return [{
            "content": content,
            "metadata": {
                "source": os.path.basename(file_path),
                "file_type": "docx"
            }
        }]

    @staticmethod
    def load_txt(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return [{
            "content": content,
            "metadata": {
                "source": os.path.basename(file_path),
                "file_type": "txt"
            }
        }]

class LoaderFactory:
    """Professional Factory to handle multi-format document ingestion."""
    _LOADERS = {
        ".pdf": DocumentLoader.load_pdf,
        ".csv": DocumentLoader.load_table,
        ".xlsx": DocumentLoader.load_table,
        ".xls": DocumentLoader.load_table,
        ".docx": DocumentLoader.load_docx,
        ".txt": DocumentLoader.load_txt
    }

    @classmethod
    def load(cls, file_path: str) -> List[Dict[str, Any]]:
        ext = os.path.splitext(file_path)[1].lower()
        loader_func = cls._LOADERS.get(ext)
        if not loader_func:
            logger.error(f"Unsupported file type: {ext}")
            raise ValueError(f"Unsupported file type: {ext}")
            
        logger.info(f"Ingesting {ext} document", path=file_path)
        return loader_func(file_path)
