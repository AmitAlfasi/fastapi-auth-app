"""
Configuration management module for the FastAPI authentication application.
This module handles environment variables, application settings, and configuration
management using Pydantic settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings and configuration management.

    This class manages all application settings including:
    - JWT authentication settings
    - Database configuration
    - Email service settings
    - Security and CORS settings

    All settings can be configured through environment variables or a .env file.
    """

    # JWT Settings
    JWT_SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


    # Email Code
    VERIFICATION_CODE_EXPIRE_MINUTES: int = 8

    # Database Settings
    DATABASE_URL: str = "sqlite:///./backend/app/app.db"

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

    # Proper model config for pydantic-settings v2
    model_config: SettingsConfigDict = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow"
    }

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching.

    Returns:
        Settings: Cached instance of application settings
    """
    return Settings() # type: ignore
