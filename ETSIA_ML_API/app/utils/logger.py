"""
Configuration du logging
"""
import logging
import sys
from app.config import settings


def setup_logger(name: str) -> logging.Logger:
    """
    Configure et retourne un logger
    
    Args:
        name: Nom du logger
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    
    # Éviter les doublons
    if logger.handlers:
        return logger
    
    # Niveau de log
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Handler console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


# Logger par défaut
logger = setup_logger(__name__)
