# 🧪 Tests Postman - API Détection de Dépression

Guide rapide pour tester l'API avec Postman.

---

## 🚀 Démarrage

### 1. Lancer Ollama
```powershell
ollama serve
```

### 2. Lancer l'API
```powershell
.\venv_test\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

---

## 📋 Tests Postman

### Test 1 : Health Check
- **Method:** `GET`
- **URL:** `http://localhost:8000/health`

**Réponse attendue :**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "...",
  "models": {
    "total": 1,
    "available": ["yansnet-llm"],
    "health": {...}
  }
}
```

---

### Test 2 : Lister les Modèles
- **Method:** `GET`
- **URL:** `http://localhost:8000/api/v1/models`

**Réponse attendue :**
```json
{
  "models": {
    "yansnet-llm": {
      "name": "yansnet-llm",
      "version": "1.0.0",
      "author": "Équipe YANSNET",
      "is_default": true
    }
  },
  "total": 1,
  "default": "yansnet-llm"
}
```

---

### Test 3 : Détection de Dépression (Cas Positif)
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/v1/predict`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "text": "I feel so sad and hopeless, I don't want to live anymore",
  "include_reasoning": true
}
```

**Réponse attendue :**
```json
{
  "prediction": "DÉPRESSION",
  "confidence": 0.85,
  "severity": "Élevée",
  "reasoning": "Le texte exprime un désespoir profond...",
  "timestamp": "2025-10-17T...",
  "model_used": "yansnet-llm"
}
```

---

### Test 4 : Texte Normal (Cas Négatif)
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/v1/predict`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "text": "I'm so happy today, life is beautiful!",
  "include_reasoning": true
}
```

**Réponse attendue :**
```json
{
  "prediction": "NORMAL",
  "confidence": 0.95,
  "severity": "Aucune",
  "reasoning": "Le texte exprime des émotions positives...",
  "timestamp": "2025-10-17T...",
  "model_used": "yansnet-llm"
}
```

---

### Test 5 : Cas Ambigu
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/v1/predict`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "text": "I feel tired and empty inside",
  "include_reasoning": true
}
```

---

### Test 6 : Sans Raisonnement (Plus Rapide)
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/v1/predict`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "text": "I feel so sad",
  "include_reasoning": false
}
```

---

### Test 7 : Avec Modèle Spécifique
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/v1/predict?model_name=yansnet-llm`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "text": "Nobody understands me, I'm alone",
  "include_reasoning": true
}
```

---

### Test 8 : Batch Prediction
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/v1/batch-predict`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "texts": [
    "I'm so happy today",
    "I feel worthless and empty",
    "Just finished a great workout"
  ],
  "include_reasoning": false
}
```

**Réponse attendue :**
```json
{
  "results": [
    {
      "text": "I'm so happy today",
      "prediction": "NORMAL",
      "confidence": 0.95,
      "severity": "Aucune"
    },
    {
      "text": "I feel worthless and empty",
      "prediction": "DÉPRESSION",
      "confidence": 0.88,
      "severity": "Élevée"
    },
    {
      "text": "Just finished a great workout",
      "prediction": "NORMAL",
      "confidence": 0.92,
      "severity": "Aucune"
    }
  ],
  "total_processed": 3,
  "processing_time": 5.2,
  "model_used": "yansnet-llm"
}
```

---

## 🔧 Dépannage

### Erreur : Connection Refused
➡️ Vérifiez qu'Ollama est lancé : `ollama serve`

### Erreur : Timeout
➡️ Le modèle llama3.2:8b est lent. Utilisez un modèle plus petit :
```powershell
ollama pull llama3.2:1b
```
Puis modifiez `.env` :
```
OLLAMA_MODEL=llama3.2:1b
```

### Erreur : Model Not Found
➡️ Téléchargez le modèle :
```powershell
ollama pull llama3.2
```

---

## 📊 Exemples de Textes à Tester

### Dépression Claire
- "I feel so sad and hopeless, I don't want to live anymore"
- "I can't stop crying, everything feels meaningless"
- "Life has no meaning, I feel worthless"
- "I hate myself, I wish I could disappear"

### Normal
- "I'm so happy today, life is beautiful"
- "Had an amazing day at work"
- "Looking forward to the weekend"
- "Just finished a great workout"

### Ambigus
- "I'm tired today"
- "I feel a bit down"
- "I can't do this anymore"
- "Nobody understands me"

---

## 🎯 Collection Postman

Vous pouvez importer cette collection dans Postman :

1. Créer une nouvelle collection "Depression Detection API"
2. Ajouter les 8 requêtes ci-dessus
3. Définir une variable d'environnement : `base_url = http://localhost:8000`

---

**Bon test ! 🚀**
