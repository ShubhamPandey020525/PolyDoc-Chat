import fitz  # PyMuPDF
import pandas as pd
from docx import Document
from typing import List, Dict, Any
import os
from src_ai.core.logger import logger

class DocumentLoader:
    """Consolidated document loader for all professional file types."""
    
    @staticmethod
    def load_pdf(file_path: str) -> List[Dict[str, Any]]:
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

    @staticmethod
    def load_table(file_path: str) -> List[Dict[str, Any]]:
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

    @staticmethod
    def load_docx(file_path: str) -> List[Dict[str, Any]]:
        doc = Document(file_path)
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
