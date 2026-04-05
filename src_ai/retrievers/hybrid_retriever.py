import asyncio
from langchain_chroma import Chroma
from src_ai.models.embedder import Embedder
from src_ai.core.config import settings
from rank_bm25 import BM25Okapi
from typing import List, Dict, Any

class HybridRetriever:
    """Professional Vector + Keyword Hybrid Retriever with Parallel Processing."""
    
    def __init__(self, persist_directory: str = settings.CHROMA_DB_PATH):
        self.embedder = Embedder()
        self.db = Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embedder.embeddings,
            persist_directory=persist_directory
        )
        self.bm25 = None
        self.data_store = []

    async def add_documents(self, data: List[Dict[str, Any]]):
        """Async-friendly document addition."""
        loop = asyncio.get_event_loop()
        texts = [d["content"] for d in data]
        metadatas = [d["metadata"] for d in data]
        
        await loop.run_in_executor(None, lambda: self.db.add_texts(texts=texts, metadatas=metadatas))
        
        # Setup BM25
        self.data_store.extend(data)
        tokenized_corpus = [d["content"].split() for d in self.data_store]
        self.bm25 = BM25Okapi(tokenized_corpus)

    async def _vector_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Async-wrapped semantic search."""
        loop = asyncio.get_event_loop()
        vector_results = await loop.run_in_executor(
            None, 
            lambda: self.db.similarity_search_with_score(query, k=top_k)
        )
        formatted = []
        for doc, score in vector_results:
            formatted.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score,
                "type": "vector"
            })
        return formatted

    async def _keyword_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Async-wrapped keyword search."""
        if not self.bm25:
            return []
            
        loop = asyncio.get_event_loop()
        tokenized_query = query.split()
        bm25_scores = await loop.run_in_executor(
            None,
            lambda: self.bm25.get_scores(tokenized_query)
        )
        
        top_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_k]
        formatted = []
        for i in top_indices:
            formatted.append({
                "content": self.data_store[i]["content"],
                "metadata": self.data_store[i]["metadata"],
                "score": float(bm25_scores[i]),
                "type": "keyword"
            })
        return formatted

    async def search(self, query: str, top_k: int = settings.RETRIEVAL_TOP_K) -> List[Dict[str, Any]]:
        """Run Semantic and Keyword search in PARALLEL using asyncio.gather."""
        vector_task = self._vector_search(query, top_k)
        keyword_task = self._keyword_search(query, top_k)
        
        # Parallel execution
        vector_results, keyword_results = await asyncio.gather(vector_task, keyword_task)
            
        # 3. Deduplicated Merge
        seen = set()
        merged = []
        for res in vector_results + keyword_results:
            content_hash = hash(res["content"])
            if content_hash not in seen:
                merged.append(res)
                seen.add(content_hash)
        
        return merged[:top_k]
