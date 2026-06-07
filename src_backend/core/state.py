from typing import Optional
from src_ai.retrievers.simple_retriever import SimpleRetriever
from src_ai.services.rag_service import GrokQueryEngine

# Global instances for the backend application
retriever: Optional[SimpleRetriever] = None
engine: Optional[GrokQueryEngine] = None
