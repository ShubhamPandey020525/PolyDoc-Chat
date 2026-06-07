from langchain_huggingface import HuggingFaceEmbeddings
from src_ai.core.config import settings
from typing import List

class Embedder:
    """Professional Embedding Generator using Local HuggingFace Models.
    Fixes '429 Too Many Requests' by running search locally on your CPU/GPU.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'} # Change to 'cuda' if you have a GPU
        )

    def embed_query(self, query: str) -> List[float]:
        return self.embeddings.embed_query(query)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(documents)
