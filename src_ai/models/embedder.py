from langchain_openai import OpenAIEmbeddings
from src_ai.core.config import settings
from typing import List

class Embedder:
    """Professional Embedding Generator using OpenAI APIs."""
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.embeddings = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def embed_query(self, query: str) -> List[float]:
        return self.embeddings.embed_query(query)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(documents)
