"""
Configuration de l'application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # LLM Provider
    LLM_PROVIDER: str = "gpt"  # gpt, claude, local
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    
    # API
    API_TITLE: str = "Depression Detection API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API de détection de dépression utilisant des LLM"
    LOG_LEVEL: str = "INFO"
    
    # Security (optionnel)
    API_KEY: Optional[str] = None
    CORS_ORIGINS: str = "*"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instance globale
settings = Settings()
