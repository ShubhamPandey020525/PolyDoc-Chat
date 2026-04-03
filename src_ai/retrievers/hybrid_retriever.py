from langchain_community.vectorstores import Chroma
from src_ai.models.embedder import Embedder
from src_ai.core.config import settings
from rank_bm25 import BM25Okapi
from typing import List, Dict, Any

class HybridRetriever:
    """Professional Vector + Keyword Hybrid Retriever."""
    
    def __init__(self, persist_directory: str = settings.CHROMA_DB_PATH):
        self.embedder = Embedder()
        self.db = Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embedder.embeddings,
            persist_directory=persist_directory
        )
        self.bm25 = None
        self.data_store = []

    def add_documents(self, data: List[Dict[str, Any]]):
        texts = [d["content"] for d in data]
        metadatas = [d["metadata"] for d in data]
        self.db.add_texts(texts=texts, metadatas=metadatas)
        self.db.persist()
        
        # Setup BM25
        self.data_store.extend(data)
        tokenized_corpus = [d["content"].split() for d in self.data_store]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, top_k: int = settings.RETRIEVAL_TOP_K) -> List[Dict[str, Any]]:
        # 1. Semantic Search
        vector_results = self.db.similarity_search_with_score(query, k=top_k)
        formatted_vector = []
        for doc, score in vector_results:
            formatted_vector.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score,
                "type": "vector"
            })
            
        # 2. Keyword Search
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_k]
        formatted_keyword = []
        for i in top_indices:
            formatted_keyword.append({
                "content": self.data_store[i]["content"],
                "metadata": self.data_store[i]["metadata"],
                "score": float(bm25_scores[i]),
                "type": "keyword"
            })
            
        # 3. Deduplicated Merge
        seen = set()
        merged = []
        for res in formatted_vector + formatted_keyword:
            content_hash = hash(res["content"])
            if content_hash not in seen:
                merged.append(res)
                seen.add(content_hash)
        
        return merged[:top_k]
