from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Code Analyzer API"
    API_V1_STR: str = "/api/v1"
    
    # Security (JWT)
    SECRET_KEY: str = "super-secret-key-change-this-in-production-environment"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "code_analyzer_db"
    
    # LLM (OpenAI)
    OPENAI_API_KEY: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
