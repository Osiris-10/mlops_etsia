"""
Modèle YANSNET - Détection de dépression avec LLM
"""
from typing import Dict, Any, List
from app.core.base_model import BaseDepressionModel
from app.services.yansnet_llm.llm_predictor import get_llm_predictor
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class YansnetLLMModel(BaseDepressionModel):
    """
    Modèle de détection de dépression utilisant des LLM.
    
    Supporte:
    - OpenAI GPT (gpt-4o-mini, gpt-4o)
    - Anthropic Claude (claude-3-5-sonnet)
    - Ollama local (llama3.2, mistral, etc.)
    """
    
    @property
    def model_name(self) -> str:
        return "yansnet-llm"
    
    @property
    def model_version(self) -> str:
        return "1.0.0"
    
    @property
    def author(self) -> str:
        return "Équipe YANSNET"
    
    @property
    def description(self) -> str:
        provider = settings.LLM_PROVIDER
        if provider == "gpt":
            model = settings.OPENAI_MODEL
        elif provider == "claude":
            model = settings.ANTHROPIC_MODEL
        else:
            model = settings.OLLAMA_MODEL
        
        return f"Détection de dépression avec LLM ({provider}: {model})"
    
    @property
    def tags(self) -> List[str]:
        return ["llm", "gpt", "claude", "ollama", "prompt-engineering"]
    
    def __init__(self):
        """Initialise le prédicteur LLM"""
        try:
            self.predictor = get_llm_predictor()
            self._initialized = True
            logger.info(f"✓ {self.model_name} initialisé avec succès")
        except Exception as e:
            logger.error(f"✗ Erreur d'initialisation de {self.model_name}: {e}")
            self._initialized = False
            raise
    
    def predict(self, text: str, include_reasoning: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Prédit si le texte indique de la dépression.
        
        Args:
            text: Texte à analyser
            include_reasoning: Inclure l'explication (défaut: True)
            **kwargs: Paramètres additionnels (ignorés)
        
        Returns:
            Dict avec prediction, confidence, severity, reasoning
        
        Raises:
            RuntimeError: Si le modèle n'est pas initialisé
        """
        if not self._initialized:
            raise RuntimeError(f"{self.model_name} n'est pas initialisé correctement")
        
        try:
            # Appeler le LLM
            result = self.predictor.predict(text)
            
            # Retirer le reasoning si non demandé
            if not include_reasoning:
                result.pop('reasoning', None)
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur de prédiction {self.model_name}: {e}")
            raise
    
    def batch_predict(self, texts: List[str], include_reasoning: bool = False, **kwargs) -> List[Dict[str, Any]]:
        """
        Prédiction batch optimisée.
        
        Args:
            texts: Liste de textes
            include_reasoning: Inclure les explications (défaut: False pour performance)
            **kwargs: Paramètres additionnels
        
        Returns:
            Liste de résultats
        """
        logger.info(f"Prédiction batch de {len(texts)} textes avec {self.model_name}")
        
        results = []
        for i, text in enumerate(texts, 1):
            try:
                result = self.predict(text, include_reasoning=include_reasoning, **kwargs)
                results.append(result)
                
                if i % 10 == 0:
                    logger.debug(f"  Traité {i}/{len(texts)} textes")
                    
            except Exception as e:
                logger.error(f"Erreur sur texte {i}: {e}")
                # Ajouter un résultat d'erreur
                results.append({
                    "prediction": "ERREUR",
                    "confidence": 0.0,
                    "severity": "Aucune",
                    "reasoning": f"Erreur: {str(e)}"
                })
        
        return results
    
    def health_check(self) -> Dict[str, Any]:
        """
        Vérifie que le modèle est opérationnel.
        
        Returns:
            Dict avec status et détails
        """
        try:
            # Test avec un texte simple
            result = self.predict("test", include_reasoning=False)
            
            return {
                "status": "healthy",
                "model": self.model_name,
                "version": self.model_version,
                "provider": settings.LLM_PROVIDER,
                "test_prediction": result.get("prediction")
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "model": self.model_name,
                "error": str(e)
            }
