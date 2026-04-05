from typing import Optional
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from src_ai.services.rag_service import GrokQueryEngine

# Global instances for the backend application
hybrid_retriever: Optional[HybridRetriever] = None
engine: Optional[GrokQueryEngine] = None
