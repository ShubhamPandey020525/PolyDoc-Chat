import cohere
from typing import List, Dict, Any
from src_ai.core.config import settings
from src_ai.core.logger import logger

class Reranker:
    """Professional API-based reranking using Cohere (Async)."""
    def __init__(self, api_key: str = settings.COHERE_API_KEY, model: str = settings.RERANKER_MODEL):
        if not api_key:
            logger.warning("COHERE_API_KEY not found. Reranking will be disabled.")
            self.async_client = None
        else:
            self.async_client = cohere.AsyncClient(api_key)
        self.model = model

    async def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = settings.RERANK_TOP_K) -> List[Dict[str, Any]]:
        if not self.async_client or not documents:
            logger.info("Skipping rerank: no client or no documents.")
            return documents[:top_k]

        doc_contents = [doc["content"] for doc in documents]
        try:
            # Using async rerank
            results = await self.async_client.rerank(
                query=query,
                documents=doc_contents,
                top_n=top_k,
                model=self.model
            )
            
            reranked_docs = []
            for result in results.results:
                original_doc = documents[result.index]
                original_doc["rerank_score"] = result.relevance_score
                reranked_docs.append(original_doc)
            
            return reranked_docs
        except Exception as e:
            logger.error("Cohere Rerank failed", error=str(e))
            return documents[:top_k]
