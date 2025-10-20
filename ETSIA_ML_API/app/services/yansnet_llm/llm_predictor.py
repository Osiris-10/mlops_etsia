"""
Prédicteurs LLM (code déplacé depuis llm_service.py)
"""
import json
from typing import Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


# ============================================================================
# PROMPTS OPTIMISÉS
# ============================================================================

SYSTEM_PROMPT = """Analyse le texte et détecte les signes de dépression.

DÉPRESSION: désespoir, pensées suicidaires, vide, inutilité, isolement
NORMAL: émotions passagères, fatigue physique, stress temporaire, positivité

Réponds en JSON:
{
    "prediction": "DÉPRESSION" ou "NORMAL",
    "confidence": 0.0 à 1.0,
    "reasoning": "Explication courte (max 50 mots)",
    "severity": "Aucune", "Faible", "Moyenne", "Élevée", "Critique"
}"""


USER_PROMPT_TEMPLATE = """Analyse ce texte:

"{text}"

Réponds en JSON uniquement."""


# ============================================================================
# PRÉDICTEURS LLM
# ============================================================================

class BaseLLMPredictor:
    """Classe de base pour les prédicteurs LLM"""
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Prédit si le texte indique de la dépression"""
        raise NotImplementedError


class GPTPredictor(BaseLLMPredictor):
    """Prédicteur avec GPT (OpenAI)"""
    
    def __init__(self):
        from openai import OpenAI
        
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY non définie dans .env")
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        logger.info(f"✓ GPT Predictor initialisé (modèle: {self.model})")
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Prédit avec GPT"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.debug(f"Prédiction GPT: {result['prediction']} (confiance: {result['confidence']})")
            return result
            
        except Exception as e:
            logger.error(f"Erreur GPT: {e}")
            return {
                "prediction": "ERREUR",
                "confidence": 0.0,
                "reasoning": f"Erreur: {str(e)}",
                "severity": "Aucune"
            }


class ClaudePredictor(BaseLLMPredictor):
    """Prédicteur avec Claude (Anthropic)"""
    
    def __init__(self):
        import anthropic
        
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY non définie dans .env")
        
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.ANTHROPIC_MODEL
        logger.info(f"✓ Claude Predictor initialisé (modèle: {self.model})")
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Prédit avec Claude"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)}
                ]
            )
            
            result = json.loads(message.content[0].text)
            logger.debug(f"Prédiction Claude: {result['prediction']} (confiance: {result['confidence']})")
            return result
            
        except Exception as e:
            logger.error(f"Erreur Claude: {e}")
            return {
                "prediction": "ERREUR",
                "confidence": 0.0,
                "reasoning": f"Erreur: {str(e)}",
                "severity": "Aucune"
            }


class LocalLLMPredictor(BaseLLMPredictor):
    """Prédicteur avec LLM local (Ollama)"""
    
    def __init__(self):
        import requests
        
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        
        # Vérifier que Ollama est accessible
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            logger.info(f"✓ Local LLM Predictor initialisé (modèle: {self.model})")
        except Exception as e:
            raise ValueError(f"Ollama non accessible à {self.base_url}: {e}")
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Prédit avec LLM local"""
        try:
            import requests
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)}
                    ],
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 200  # Limiter la longueur de réponse
                    }
                },
                timeout=120  # Augmenter le timeout à 2 minutes
            )
            response.raise_for_status()
            
            result = json.loads(response.json()['message']['content'])
            logger.debug(f"Prédiction Local: {result['prediction']} (confiance: {result['confidence']})")
            return result
            
        except Exception as e:
            logger.error(f"Erreur Local LLM: {e}")
            return {
                "prediction": "ERREUR",
                "confidence": 0.0,
                "reasoning": f"Erreur: {str(e)}",
                "severity": "Aucune"
            }


# ============================================================================
# FACTORY
# ============================================================================

def get_llm_predictor() -> BaseLLMPredictor:
    """
    Retourne le prédicteur LLM configuré.
    
    Returns:
        Instance du prédicteur
    
    Raises:
        ValueError: Si le provider n'est pas supporté
    """
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "gpt":
        return GPTPredictor()
    elif provider == "claude":
        return ClaudePredictor()
    elif provider == "local":
        return LocalLLMPredictor()
    else:
        raise ValueError(f"Provider LLM non supporté: {provider}")
