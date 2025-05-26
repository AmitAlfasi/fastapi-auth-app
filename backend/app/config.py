from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
from pydantic import ConfigDict

class Settings(BaseSettings):
    # JWT Settings
    JWT_SECRET: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Mail Settings (for backward compatibility)
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None
    
    # Security Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"  # Allow extra fields from .env
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
