"""
Interface de base pour tous les modèles de détection de dépression
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseDepressionModel(ABC):
    """
    Interface que tous les modèles doivent implémenter.
    
    Chaque étudiant doit créer une classe qui hérite de celle-ci
    et implémente toutes les méthodes abstraites.
    """
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Nom unique du modèle (ex: 'yansnet-llm', 'etudiant2-gcn')
        
        Format recommandé: 'nom_equipe-type_modele'
        """
        pass
    
    @property
    @abstractmethod
    def model_version(self) -> str:
        """Version du modèle (ex: '1.0.0')"""
        pass
    
    @property
    @abstractmethod
    def author(self) -> str:
        """Auteur ou équipe (ex: 'Équipe YANSNET')"""
        pass
    
    @property
    def description(self) -> str:
        """Description du modèle (optionnel)"""
        return "Modèle de détection de dépression"
    
    @property
    def tags(self) -> List[str]:
        """Tags pour catégoriser le modèle (optionnel)"""
        return []
    
    @abstractmethod
    def predict(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Prédit si le texte indique de la dépression.
        
        Args:
            text: Texte à analyser
            **kwargs: Paramètres additionnels spécifiques au modèle
        
        Returns:
            Dict avec AU MINIMUM:
            {
                "prediction": str,  # "DÉPRESSION" ou "NORMAL"
                "confidence": float,  # 0.0 à 1.0
                "severity": str,  # "Aucune", "Faible", "Moyenne", "Élevée", "Critique"
                "reasoning": str (optionnel)  # Explication
            }
        
        Raises:
            Exception: Si la prédiction échoue
        """
        pass
    
    def batch_predict(self, texts: List[str], **kwargs) -> List[Dict[str, Any]]:
        """
        Prédiction batch (implémentation par défaut).
        
        Les modèles peuvent override cette méthode pour optimiser
        le traitement batch.
        
        Args:
            texts: Liste de textes
            **kwargs: Paramètres additionnels
        
        Returns:
            Liste de résultats (même format que predict)
        """
        return [self.predict(text, **kwargs) for text in texts]
    
    def get_info(self) -> Dict[str, Any]:
        """
        Retourne les informations sur le modèle.
        
        Returns:
            Dict avec métadonnées du modèle
        """
        return {
            "name": self.model_name,
            "version": self.model_version,
            "author": self.author,
            "description": self.description,
            "tags": self.tags
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Vérifie que le modèle est opérationnel.
        
        Returns:
            Dict avec status et détails
        """
        try:
            # Test simple avec un texte court
            result = self.predict("test")
            return {
                "status": "healthy",
                "model": self.model_name,
                "version": self.model_version
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "model": self.model_name,
                "error": str(e)
            }
