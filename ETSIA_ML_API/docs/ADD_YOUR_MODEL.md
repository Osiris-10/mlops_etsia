# 🎓 Guide : Ajouter Votre Modèle

Guide complet pour les étudiants qui veulent ajouter leur propre modèle de détection de dépression.

---

## 📋 Vue d'Ensemble

L'API utilise une **architecture multi-modèles** qui permet à chaque étudiant d'ajouter son propre modèle sans conflit avec les autres.

### Principe

Chaque modèle est dans son propre dossier :
```
app/services/
├── yansnet_llm/          # Modèle de l'équipe YANSNET
├── votre_modele/         # VOTRE modèle ici
└── autre_etudiant/       # Modèle d'un autre étudiant
```

---

## 🚀 Étapes pour Ajouter Votre Modèle

### 1. Créer la Structure

```bash
# Créer votre dossier
mkdir app/services/votre_nom_modele

# Créer les fichiers nécessaires
touch app/services/votre_nom_modele/__init__.py
touch app/services/votre_nom_modele/votre_nom_model.py
touch app/services/votre_nom_modele/requirements.txt
```

### 2. Implémenter l'Interface

Créer `app/services/votre_nom_modele/votre_nom_model.py` :

```python
"""
Votre modèle de détection de dépression
"""
from typing import Dict, Any, List
from app.core.base_model import BaseDepressionModel
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class VotreNomModel(BaseDepressionModel):
    """
    Description de votre modèle.
    
    Exemple: Modèle GCN avec embeddings BERT
    """
    
    # ========================================================================
    # PROPRIÉTÉS OBLIGATOIRES
    # ========================================================================
    
    @property
    def model_name(self) -> str:
        """Nom unique (format: nom_equipe-type)"""
        return "votre_nom-gcn"  # Exemple: "dupont-gcn", "martin-lstm"
    
    @property
    def model_version(self) -> str:
        """Version du modèle"""
        return "1.0.0"
    
    @property
    def author(self) -> str:
        """Votre nom ou équipe"""
        return "Votre Nom"
    
    @property
    def description(self) -> str:
        """Description courte"""
        return "Modèle GCN avec embeddings BERT pour détection de dépression"
    
    @property
    def tags(self) -> List[str]:
        """Tags pour catégoriser"""
        return ["gcn", "bert", "graph-neural-network"]
    
    # ========================================================================
    # INITIALISATION
    # ========================================================================
    
    def __init__(self):
        """
        Initialisez votre modèle ici.
        
        Chargez les poids, configurez les paramètres, etc.
        """
        try:
            # Exemple: charger un modèle PyTorch
            # self.model = torch.load('path/to/model.pt')
            # self.tokenizer = AutoTokenizer.from_pretrained('bert-base')
            
            logger.info(f"✓ {self.model_name} initialisé")
            self._initialized = True
            
        except Exception as e:
            logger.error(f"✗ Erreur d'initialisation: {e}")
            self._initialized = False
            raise
    
    # ========================================================================
    # MÉTHODE OBLIGATOIRE: PREDICT
    # ========================================================================
    
    def predict(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Prédit si le texte indique de la dépression.
        
        Args:
            text: Texte à analyser
            **kwargs: Paramètres additionnels (optionnels)
        
        Returns:
            Dict avec AU MINIMUM:
            {
                "prediction": "DÉPRESSION" ou "NORMAL",
                "confidence": float (0.0 à 1.0),
                "severity": "Aucune"|"Faible"|"Moyenne"|"Élevée"|"Critique",
                "reasoning": str (optionnel)
            }
        """
        if not self._initialized:
            raise RuntimeError(f"{self.model_name} non initialisé")
        
        try:
            # VOTRE CODE ICI
            # Exemple:
            # 1. Prétraiter le texte
            # processed = self.preprocess(text)
            
            # 2. Générer embeddings
            # embeddings = self.get_embeddings(processed)
            
            # 3. Prédire avec votre modèle
            # output = self.model(embeddings)
            # prediction = "DÉPRESSION" if output > 0.5 else "NORMAL"
            # confidence = float(output)
            
            # Pour l'exemple, retournons un résultat fictif
            prediction = "NORMAL"
            confidence = 0.75
            severity = "Aucune"
            reasoning = "Analyse basée sur GCN avec embeddings BERT"
            
            return {
                "prediction": prediction,
                "confidence": confidence,
                "severity": severity,
                "reasoning": reasoning
            }
            
        except Exception as e:
            logger.error(f"Erreur de prédiction: {e}")
            raise
    
    # ========================================================================
    # MÉTHODE OPTIONNELLE: BATCH_PREDICT
    # ========================================================================
    
    def batch_predict(self, texts: List[str], **kwargs) -> List[Dict[str, Any]]:
        """
        Prédiction batch (optionnel, mais recommandé pour performance).
        
        Si non implémenté, l'implémentation par défaut appelle predict()
        pour chaque texte.
        """
        # Implémentation par défaut (peut être optimisée)
        return [self.predict(text, **kwargs) for text in texts]
        
        # OU implémentation optimisée:
        # results = []
        # embeddings = self.batch_get_embeddings(texts)
        # outputs = self.model(embeddings)
        # for output in outputs:
        #     results.append({...})
        # return results
```

### 3. Créer __init__.py

Créer `app/services/votre_nom_modele/__init__.py` :

```python
"""
Votre modèle
"""
from .votre_nom_model import VotreNomModel

__all__ = ['VotreNomModel']
```

### 4. Ajouter les Dépendances

Créer `app/services/votre_nom_modele/requirements.txt` :

```txt
# Dépendances spécifiques à votre modèle
torch>=2.0.0
torch-geometric>=2.3.0
transformers>=4.30.0
scikit-learn>=1.3.0
```

### 5. Enregistrer le Modèle

Modifier `app/main.py` pour enregistrer votre modèle :

```python
@app.on_event("startup")
async def startup_event():
    # ... code existant ...
    
    # Ajouter votre modèle
    try:
        from app.services.votre_nom_modele import VotreNomModel
        registry.register(VotreNomModel())
        logger.info("✓ Votre modèle enregistré")
    except Exception as e:
        logger.error(f"✗ Erreur: {e}")
```

### 6. Installer et Tester

```bash
# Installer vos dépendances
pip install -r app/services/votre_nom_modele/requirements.txt

# Lancer l'API
uvicorn app.main:app --reload

# Tester votre modèle
curl http://localhost:8000/api/v1/models

curl -X POST "http://localhost:8000/api/v1/predict?model_name=votre_nom-gcn" \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel sad"}'
```

---

## 📝 Exemple Complet : Modèle GCN

Voici un exemple complet d'un modèle GCN :

```python
"""
Modèle GCN de Jean Dupont
"""
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from typing import Dict, Any, List
from app.core.base_model import BaseDepressionModel
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DupontGCNModel(BaseDepressionModel):
    """Modèle GCN avec embeddings BERT"""
    
    @property
    def model_name(self) -> str:
        return "dupont-gcn"
    
    @property
    def model_version(self) -> str:
        return "1.0.0"
    
    @property
    def author(self) -> str:
        return "Jean Dupont"
    
    @property
    def description(self) -> str:
        return "GCN avec BERT embeddings et attention mechanism"
    
    @property
    def tags(self) -> List[str]:
        return ["gcn", "bert", "attention", "graph-neural-network"]
    
    def __init__(self, model_path: str = "./models/dupont_gcn.pt"):
        """Initialise le modèle GCN"""
        try:
            # Charger BERT
            self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
            self.bert = AutoModel.from_pretrained("bert-base-uncased")
            
            # Charger le modèle GCN
            self.gcn_model = torch.load(model_path)
            self.gcn_model.eval()
            
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.bert.to(self.device)
            self.gcn_model.to(self.device)
            
            logger.info(f"✓ {self.model_name} initialisé sur {self.device}")
            self._initialized = True
            
        except Exception as e:
            logger.error(f"✗ Erreur d'initialisation: {e}")
            self._initialized = False
            raise
    
    def get_embeddings(self, text: str) -> torch.Tensor:
        """Génère les embeddings BERT"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.bert(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        
        return embeddings
    
    def predict(self, text: str, **kwargs) -> Dict[str, Any]:
        """Prédit avec le GCN"""
        if not self._initialized:
            raise RuntimeError(f"{self.model_name} non initialisé")
        
        try:
            # 1. Générer embeddings
            embeddings = self.get_embeddings(text)
            
            # 2. Prédire avec GCN
            with torch.no_grad():
                output = self.gcn_model(embeddings)
                probs = torch.softmax(output, dim=1)
                pred_class = torch.argmax(probs, dim=1).item()
                confidence = probs[0, pred_class].item()
            
            # 3. Interpréter
            prediction = "DÉPRESSION" if pred_class == 1 else "NORMAL"
            
            # Déterminer sévérité
            if prediction == "DÉPRESSION":
                if confidence > 0.9:
                    severity = "Élevée"
                elif confidence > 0.7:
                    severity = "Moyenne"
                else:
                    severity = "Faible"
            else:
                severity = "Aucune"
            
            return {
                "prediction": prediction,
                "confidence": float(confidence),
                "severity": severity,
                "reasoning": f"Analyse GCN avec confiance {confidence:.2%}"
            }
            
        except Exception as e:
            logger.error(f"Erreur de prédiction: {e}")
            raise
```

---

## 🧪 Tests

Créer `tests/test_votre_modele.py` :

```python
"""
Tests pour votre modèle
"""
import pytest
from app.services.votre_nom_modele import VotreNomModel


def test_model_initialization():
    """Test d'initialisation"""
    model = VotreNomModel()
    assert model.model_name == "votre_nom-gcn"
    assert model.model_version == "1.0.0"


def test_model_predict():
    """Test de prédiction"""
    model = VotreNomModel()
    result = model.predict("I feel sad")
    
    assert "prediction" in result
    assert "confidence" in result
    assert "severity" in result
    assert result["prediction"] in ["DÉPRESSION", "NORMAL"]
    assert 0 <= result["confidence"] <= 1


def test_model_batch_predict():
    """Test de prédiction batch"""
    model = VotreNomModel()
    texts = ["I'm happy", "I feel sad"]
    results = model.batch_predict(texts)
    
    assert len(results) == 2
    for result in results:
        assert "prediction" in result
```

---

## 📋 Checklist

Avant de push votre modèle :

- [ ] Dossier créé : `app/services/votre_nom_modele/`
- [ ] Classe implémente `BaseDepressionModel`
- [ ] Méthode `predict()` retourne le bon format
- [ ] `requirements.txt` avec vos dépendances
- [ ] Modèle enregistré dans `app/main.py`
- [ ] Tests écrits et passent
- [ ] Documentation ajoutée (docstrings)
- [ ] Pas de secrets dans le code (clés API, etc.)

---

## 🤝 Bonnes Pratiques

### Nommage

- **Nom du modèle** : `nom_equipe-type` (ex: `dupont-gcn`, `martin-lstm`)
- **Dossier** : `app/services/nom_equipe_type/`
- **Classe** : `NomEquipeTypeModel` (ex: `DupontGCNModel`)

### Performance

- Implémenter `batch_predict()` pour optimiser
- Utiliser `@torch.no_grad()` pour l'inférence
- Charger le modèle une seule fois (dans `__init__`)

### Erreurs

- Toujours logger les erreurs
- Retourner un résultat même en cas d'erreur
- Ne pas faire crasher l'API

### Documentation

- Docstrings claires
- Expliquer les paramètres
- Donner des exemples

---

## ❓ FAQ

### Q: Mon modèle utilise PyTorch, un autre utilise TensorFlow. Problème ?

**R:** Non ! Chaque modèle a ses propres dépendances dans son `requirements.txt`.

### Q: Comment gérer les fichiers de modèle volumineux ?

**R:** 
1. Ne PAS les commit dans git
2. Les stocker ailleurs (Google Drive, S3)
3. Télécharger au premier lancement
4. Ajouter au `.gitignore`

### Q: Puis-je utiliser des données externes ?

**R:** Oui, mais :
- Documenter la source
- Respecter les licences
- Ne pas commit les données volumineuses

### Q: Mon modèle est lent, que faire ?

**R:**
- Implémenter `batch_predict()` optimisé
- Utiliser GPU si disponible
- Cacher les résultats fréquents
- Optimiser le preprocessing

---

## 📞 Support

- **Documentation** : Voir les autres docs dans `docs/`
- **Exemple** : Regarder `app/services/yansnet_llm/`
- **Issues** : Créer une issue GitHub
- **Questions** : Demander à l'équipe

---

**Bon courage pour votre modèle ! 🚀**
