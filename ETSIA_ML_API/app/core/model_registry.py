"""
Registre centralisé des modèles de détection
"""
from typing import Dict, Optional, List
from app.core.base_model import BaseDepressionModel
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelRegistry:
    """
    Registre singleton pour gérer tous les modèles disponibles.
    
    Permet d'enregistrer, récupérer et lister les modèles dynamiquement.
    """
    
    _instance: Optional['ModelRegistry'] = None
    _models: Dict[str, BaseDepressionModel] = {}
    _default_model: Optional[str] = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._models = {}
            cls._instance._default_model = None
        return cls._instance
    
    def register(self, model: BaseDepressionModel, set_as_default: bool = False):
        """
        Enregistre un nouveau modèle dans le registre.
        
        Args:
            model: Instance du modèle à enregistrer
            set_as_default: Si True, définit ce modèle comme défaut
        
        Raises:
            ValueError: Si le modèle est invalide
        """
        # Validation
        if not isinstance(model, BaseDepressionModel):
            raise ValueError(f"Le modèle doit hériter de BaseDepressionModel")
        
        model_name = model.model_name
        
        # Vérifier si déjà enregistré
        if model_name in self._models:
            logger.warning(f"⚠️  Modèle '{model_name}' déjà enregistré, écrasement")
        
        # Enregistrer
        self._models[model_name] = model
        logger.info(
            f"✓ Modèle enregistré: {model_name} "
            f"v{model.model_version} by {model.author}"
        )
        
        # Définir comme défaut si demandé ou si c'est le premier
        if set_as_default or self._default_model is None:
            self._default_model = model_name
            logger.info(f"  → Défini comme modèle par défaut")
    
    def get(self, model_name: str) -> Optional[BaseDepressionModel]:
        """
        Récupère un modèle par son nom.
        
        Args:
            model_name: Nom du modèle
        
        Returns:
            Instance du modèle ou None si non trouvé
        """
        return self._models.get(model_name)
    
    def get_default(self) -> Optional[BaseDepressionModel]:
        """
        Retourne le modèle par défaut.
        
        Returns:
            Instance du modèle par défaut ou None
        """
        if self._default_model:
            return self._models.get(self._default_model)
        return None
    
    def list_models(self) -> Dict[str, Dict]:
        """
        Liste tous les modèles disponibles avec leurs métadonnées.
        
        Returns:
            Dict {model_name: model_info}
        """
        return {
            name: {
                **model.get_info(),
                "is_default": name == self._default_model
            }
            for name, model in self._models.items()
        }
    
    def get_model_names(self) -> List[str]:
        """
        Retourne la liste des noms de modèles disponibles.
        
        Returns:
            Liste des noms
        """
        return list(self._models.keys())
    
    def unregister(self, model_name: str) -> bool:
        """
        Désenregistre un modèle.
        
        Args:
            model_name: Nom du modèle à retirer
        
        Returns:
            True si retiré, False si non trouvé
        """
        if model_name in self._models:
            del self._models[model_name]
            logger.info(f"✓ Modèle désenregistré: {model_name}")
            
            # Si c'était le défaut, choisir un autre
            if self._default_model == model_name:
                self._default_model = next(iter(self._models.keys()), None)
                if self._default_model:
                    logger.info(f"  → Nouveau défaut: {self._default_model}")
            
            return True
        return False
    
    def clear(self):
        """Vide le registre (utile pour les tests)"""
        self._models.clear()
        self._default_model = None
        logger.info("✓ Registre vidé")
    
    def health_check_all(self) -> Dict[str, Dict]:
        """
        Vérifie la santé de tous les modèles.
        
        Returns:
            Dict {model_name: health_status}
        """
        return {
            name: model.health_check()
            for name, model in self._models.items()
        }


# Instance globale (singleton)
registry = ModelRegistry()
