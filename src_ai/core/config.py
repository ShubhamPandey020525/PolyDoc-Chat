import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Keys & Base URLs
    XAI_API_KEY: str = os.getenv("XAI_API_KEY", "")
    XAI_BASE_URL: str = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    
    # Model Selection
    GROK_MODEL: str = "grok-1" 
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    RERANKER_MODEL: str = "rerank-english-v3.0"
    
    # Vector DB Configuration
    CHROMA_DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "polydoc_professional_v2"
    
    # RAG Hyperparameters
    CHUNK_SIZE: int = 1200
    CHUNK_OVERLAP: int = 150
    RETRIEVAL_TOP_K: int = 15
    RERANK_TOP_K: int = 5
    
    # Infrastructure
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("APP_ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
