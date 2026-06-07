import asyncio
from langchain_chroma import Chroma
from src_ai.models.embedder import Embedder
from src_ai.core.config import settings
from typing import List, Dict, Any
import os

class SimpleRetriever:
    """Simple Similarity Search Retriever using ChromaDB."""
    
    def __init__(self, persist_directory: str = settings.CHROMA_DB_PATH):
        self.embedder = Embedder()
        self.persist_directory = persist_directory
        self.db = self._init_db()

    def _init_db(self):
        return Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embedder.embeddings,
            persist_directory=self.persist_directory
        )

    async def add_documents(self, data: List[Dict[str, Any]]):
        """Batched document addition to the vector database."""
        loop = asyncio.get_event_loop()
        batch_size = max(1, settings.INDEX_BATCH_SIZE)
        
        # Create batches
        batches = [data[i : i + batch_size] for i in range(0, len(data), batch_size)]
        
        def _add_batch(batch_data: List[Dict[str, Any]]):
            texts = [d["content"] for d in batch_data]
            metadatas = [d["metadata"] for d in batch_data]
            self.db.add_texts(texts=texts, metadatas=metadatas)
        
        # Parallel indexing
        tasks = [loop.run_in_executor(None, _add_batch, batch) for batch in batches]
        await asyncio.gather(*tasks)

    async def search(self, query: str, top_k: int = settings.RETRIEVAL_TOP_K) -> List[Dict[str, Any]]:
        """Async-wrapped semantic similarity search."""
        loop = asyncio.get_event_loop()
        
        def _sync_search():
            return self.db.similarity_search_with_score(query, k=top_k)
            
        vector_results = await loop.run_in_executor(None, _sync_search)
        
        formatted = []
        for doc, score in vector_results:
            formatted.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })
        return formatted
