from pathlib import Path
import os
from functools import lru_cache
from pydantic import BaseSettings

# Try to import dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    # Only load .env locally; Railway sets environment variables automatically
    if os.getenv("RAILWAY_ENV") is None:
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        load_dotenv(os.path.join(basedir, ".env"))
except ImportError:
    # In production, we don't need dotenv as environment variables are set differently
    pass

class Settings(BaseSettings):
    # Environment settings
    ENV: str = os.getenv("ENV", "production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ["true", "1", "yes"]
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/dbname"
    )
    
    # API Keys and tokens
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "your-telegram-bot-token")
    X_SOAX_API_SECRET: str = os.getenv("X_SOAX_API_SECRET", "your-soax-token")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-openai-key")
    TELEGRAM_API_URL: str = os.getenv("TELEGRAM_API_URL", "your-telegram-api-url")
    
    # Path settings
    BASE_DIR: Path = Path.cwd()
    LINKS_HISTORY_PATH: Path = BASE_DIR / "storage" / "links_history"
    FILES_PATH: Path = BASE_DIR / "app" / "files"
    THUMBNAILS_PATH: Path = BASE_DIR / "app" / "thumbnails"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache to avoid loading .env file for each request
    """
    return Settings() 