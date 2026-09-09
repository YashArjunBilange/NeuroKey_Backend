from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "NLP Smart Keyboard API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./nlp_keyboard.db"
    SECRET_KEY: str = "dev-only-change-this-secret"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:4173"]
    GEMINI_API_KEY: str | None = None
    GIF_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
