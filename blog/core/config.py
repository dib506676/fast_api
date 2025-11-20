"""
Application configuration settings
Loads environment variables from .env file
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Project Info
    PROJECT_NAME: str = "Blog API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    # Database - with default
    DATABASE_URL: str = "sqlite+aiosqlite:///./blog.db"
    
    # JWT Security - with default (change in production!)
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth (Optional)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()
