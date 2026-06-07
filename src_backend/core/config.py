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
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Backend Config
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: list = ["*"]
    UPLOAD_DIR: str = "uploads"
    CHROMA_DB_PATH: str = "./chroma_db"

    # AI Config
    GROK_MODEL: str = "grok-beta"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100
    RETRIEVAL_TOP_K: int = 8

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
