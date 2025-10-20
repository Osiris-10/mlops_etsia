"""
Core - Infrastructure pour le système multi-modèles
"""
from .base_model import BaseDepressionModel
from .model_registry import ModelRegistry, registry

__all__ = ['BaseDepressionModel', 'ModelRegistry', 'registry']
