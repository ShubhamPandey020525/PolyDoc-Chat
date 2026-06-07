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
    GROK_MODEL: str = "grok-beta" 
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Vector DB Configuration
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    COLLECTION_NAME: str = "polydoc_v3"
    
    # RAG Hyperparameters
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100
    RETRIEVAL_TOP_K: int = 8
    INDEX_BATCH_SIZE: int = 128
    
    # Infrastructure
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("APP_ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
