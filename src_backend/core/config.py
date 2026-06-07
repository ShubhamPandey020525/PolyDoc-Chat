import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Keys & Base URLs
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Backend Config
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: list = ["*"]
    UPLOAD_DIR: str = "uploads"
    CHROMA_DB_PATH: str = "./chroma_db"

    # AI Config
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100
    RETRIEVAL_TOP_K: int = 8

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
