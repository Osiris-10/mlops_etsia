# 📋 Contrat d'API - Détection de Dépression

Documentation complète de l'API REST pour la détection de dépression avec LLM.

---

## 🌐 Base URL

```
http://localhost:8000
```

En production, remplacer par votre domaine.

---

## 🔐 Authentification

Actuellement, l'API est ouverte. Pour ajouter une authentification :

```env
API_KEY=votre-clé-secrète
```

Puis inclure dans les headers :
```
X-API-Key: votre-clé-secrète
```

---

## 📍 Endpoints

### 1. Health Check

Vérifie l'état de l'API.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "llm_provider": "gpt",
  "llm_model": "gpt-4o-mini",
  "timestamp": "2025-01-16T10:30:00Z"
}
```

**Status Codes:**
- `200 OK` - API fonctionnelle

---

### 2. Prédiction Simple

Analyse un texte et détecte les signes de dépression.

**Endpoint:** `POST /api/v1/predict`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "I feel so sad and hopeless, I don't want to live anymore",
  "include_reasoning": true
}
```

**Parameters:**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `text` | string | ✅ | Texte à analyser (1-5000 caractères) |
| `include_reasoning` | boolean | ❌ | Inclure l'explication (défaut: true) |

**Response:**
```json
{
  "prediction": "DÉPRESSION",
  "confidence": 0.85,
  "severity": "Élevée",
  "reasoning": "Le texte exprime un désespoir profond et une tristesse intense, avec des pensées suicidaires explicites. Les marqueurs linguistiques indiquent une détresse psychologique sévère.",
  "timestamp": "2025-01-16T10:30:00Z",
  "model_used": "gpt-4o-mini"
}
```

**Response Fields:**

| Champ | Type | Description |
|-------|------|-------------|
| `prediction` | enum | `"DÉPRESSION"` ou `"NORMAL"` |
| `confidence` | float | Niveau de confiance (0.0 - 1.0) |
| `severity` | enum | `"Aucune"`, `"Faible"`, `"Moyenne"`, `"Élevée"`, `"Critique"` |
| `reasoning` | string | Explication du raisonnement (si demandé) |
| `timestamp` | datetime | Timestamp ISO 8601 |
| `model_used` | string | Modèle LLM utilisé |

**Status Codes:**
- `200 OK` - Prédiction réussie
- `400 Bad Request` - Requête invalide (texte vide, trop long, etc.)
- `500 Internal Server Error` - Erreur serveur

**Exemples de Requêtes:**

```bash
# Avec reasoning
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel so sad and hopeless",
    "include_reasoning": true
  }'

# Sans reasoning (plus rapide)
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I feel so sad and hopeless",
    "include_reasoning": false
  }'
```

**Exemples Python:**

```python
import requests

# Prédiction simple
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "text": "I feel so sad and hopeless",
        "include_reasoning": True
    }
)

result = response.json()
print(f"Prédiction: {result['prediction']}")
print(f"Confiance: {result['confidence']:.2%}")
print(f"Sévérité: {result['severity']}")
print(f"Raisonnement: {result['reasoning']}")
```

---

### 3. Prédiction Batch

Analyse plusieurs textes en une seule requête.

**Endpoint:** `POST /api/v1/batch-predict`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
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

**Parameters:**

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `texts` | array[string] | ✅ | Liste de textes (1-100 textes) |
| `include_reasoning` | boolean | ❌ | Inclure les explications (défaut: false) |

**Response:**
```json
{
  "results": [
    {
      "text": "I'm so happy today",
      "prediction": "NORMAL",
      "confidence": 0.95,
      "severity": "Aucune",
      "reasoning": null
    },
    {
      "text": "I feel worthless and empty",
      "prediction": "DÉPRESSION",
      "confidence": 0.88,
      "severity": "Élevée",
      "reasoning": null
    },
    {
      "text": "Just finished a great workout",
      "prediction": "NORMAL",
      "confidence": 0.92,
      "severity": "Aucune",
      "reasoning": null
    }
  ],
  "total_processed": 3,
  "processing_time": 1.2,
  "model_used": "gpt-4o-mini"
}
```

**Response Fields:**

| Champ | Type | Description |
|-------|------|-------------|
| `results` | array | Liste des prédictions |
| `total_processed` | integer | Nombre de textes traités |
| `processing_time` | float | Temps de traitement (secondes) |
| `model_used` | string | Modèle LLM utilisé |

**Status Codes:**
- `200 OK` - Prédictions réussies
- `400 Bad Request` - Requête invalide (liste vide, trop de textes, etc.)
- `500 Internal Server Error` - Erreur serveur

**Exemples de Requêtes:**

```bash
curl -X POST http://localhost:8000/api/v1/batch-predict \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "I am so happy today",
      "I feel worthless and empty"
    ],
    "include_reasoning": false
  }'
```

**Exemples Python:**

```python
import requests

# Prédiction batch
texts = [
    "I'm so happy today",
    "I feel worthless and empty",
    "Just finished a great workout"
]

response = requests.post(
    "http://localhost:8000/api/v1/batch-predict",
    json={
        "texts": texts,
        "include_reasoning": False
    }
)

result = response.json()
print(f"Traité {result['total_processed']} textes en {result['processing_time']:.2f}s")

for item in result['results']:
    print(f"\nTexte: {item['text']}")
    print(f"Prédiction: {item['prediction']} ({item['confidence']:.2%})")
```

---

## 🔄 Codes de Statut HTTP

| Code | Signification | Description |
|------|---------------|-------------|
| 200 | OK | Requête réussie |
| 400 | Bad Request | Requête invalide (validation échouée) |
| 422 | Unprocessable Entity | Données invalides (Pydantic validation) |
| 500 | Internal Server Error | Erreur serveur |
| 503 | Service Unavailable | Service LLM indisponible |

---

## ❌ Gestion des Erreurs

Toutes les erreurs retournent un format standard :

```json
{
  "error": "Erreur de prédiction",
  "detail": "Le service LLM est temporairement indisponible",
  "timestamp": "2025-01-16T10:30:00Z"
}
```

**Exemples d'Erreurs:**

### Texte vide
```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "Le texte ne peut pas être vide",
      "type": "value_error"
    }
  ]
}
```

### Texte trop long
```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "ensure this value has at most 5000 characters",
      "type": "value_error.any_str.max_length"
    }
  ]
}
```

### Service LLM indisponible
```json
{
  "error": "Erreur de prédiction",
  "detail": "Erreur: Connection timeout",
  "timestamp": "2025-01-16T10:30:00Z"
}
```

---

## 📊 Limites et Quotas

| Limite | Valeur | Description |
|--------|--------|-------------|
| Taille max texte | 5000 caractères | Par texte individuel |
| Batch max | 100 textes | Par requête batch |
| Rate limit | Aucun | À configurer selon vos besoins |
| Timeout | 30 secondes | Par requête |

---

## 🔧 Configuration des Providers

### GPT (OpenAI)

```env
LLM_PROVIDER=gpt
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

**Modèles disponibles:**
- `gpt-4o-mini` (recommandé) - Rapide et économique
- `gpt-4o` - Plus puissant mais plus cher
- `gpt-3.5-turbo` - Économique mais moins précis

### Claude (Anthropic)

```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Modèles disponibles:**
- `claude-3-5-sonnet-20241022` (recommandé) - Meilleur équilibre
- `claude-3-opus-20240229` - Plus puissant
- `claude-3-haiku-20240307` - Plus rapide

### Ollama (Local)

```env
LLM_PROVIDER=local
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

**Modèles disponibles:**
- `llama3.2` (recommandé) - Bon équilibre
- `llama3.1` - Plus puissant
- `mistral` - Alternative

---

## 📈 Performances

### Latence Moyenne

| Provider | Latence | Coût par requête |
|----------|---------|------------------|
| GPT-4o-mini | ~300ms | ~$0.00006 |
| Claude Sonnet | ~300ms | ~$0.00015 |
| Llama local | ~300ms | Gratuit |

### Throughput

- **Single request:** ~3 req/s
- **Batch (10 textes):** ~0.3 batch/s
- **Batch (100 textes):** ~0.03 batch/s

---

## 🧪 Tests

### Test avec curl

```bash
# Health check
curl http://localhost:8000/health

# Prédiction simple
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel so sad"}'

# Batch
curl -X POST http://localhost:8000/api/v1/batch-predict \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Happy", "Sad"]}'
```

### Test avec Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Prédiction
response = requests.post(
    f"{BASE_URL}/api/v1/predict",
    json={"text": "I feel so sad and hopeless"}
)
print(response.json())
```

---

## 📚 Documentation Interactive

L'API fournit une documentation interactive via Swagger UI :

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Ces interfaces permettent de :
- Voir tous les endpoints
- Tester les requêtes directement
- Voir les schémas de données
- Télécharger le schéma OpenAPI

---

## 🔒 Sécurité

### Recommandations

1. **HTTPS en production** - Toujours utiliser HTTPS
2. **API Key** - Ajouter une authentification par clé
3. **Rate Limiting** - Limiter le nombre de requêtes
4. **CORS** - Configurer les origines autorisées
5. **Validation** - Toutes les entrées sont validées par Pydantic

### Exemple de Configuration Sécurisée

```env
# API Key
API_KEY=votre-clé-secrète-complexe

# CORS
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# HTTPS
# Utiliser un reverse proxy (nginx, traefik)
```

---

## 📞 Support

Pour toute question sur l'API :
- **Documentation:** http://localhost:8000/docs
- **Issues:** GitHub Issues
- **Email:** Équipe YANSNET

---

**Version:** 1.0.0  
**Dernière mise à jour:** Janvier 2025
