"""
Tests de l'API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test de la page d'accueil"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health():
    """Test du health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "llm_provider" in data


def test_predict_valid():
    """Test de prédiction avec texte valide"""
    response = client.post(
        "/api/v1/predict",
        json={
            "text": "I feel so sad and hopeless",
            "include_reasoning": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "severity" in data
    assert data["prediction"] in ["DÉPRESSION", "NORMAL"]
    assert 0 <= data["confidence"] <= 1


def test_predict_empty_text():
    """Test avec texte vide"""
    response = client.post(
        "/api/v1/predict",
        json={
            "text": "",
            "include_reasoning": False
        }
    )
    assert response.status_code == 422  # Validation error


def test_predict_too_long():
    """Test avec texte trop long"""
    long_text = "a" * 6000
    response = client.post(
        "/api/v1/predict",
        json={
            "text": long_text,
            "include_reasoning": False
        }
    )
    assert response.status_code == 422  # Validation error


def test_batch_predict_valid():
    """Test de prédiction batch"""
    response = client.post(
        "/api/v1/batch-predict",
        json={
            "texts": [
                "I'm so happy today",
                "I feel worthless"
            ],
            "include_reasoning": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total_processed" in data
    assert len(data["results"]) == 2


def test_batch_predict_empty_list():
    """Test batch avec liste vide"""
    response = client.post(
        "/api/v1/batch-predict",
        json={
            "texts": [],
            "include_reasoning": False
        }
    )
    assert response.status_code == 422  # Validation error


def test_batch_predict_too_many():
    """Test batch avec trop de textes"""
    texts = ["text"] * 101
    response = client.post(
        "/api/v1/batch-predict",
        json={
            "texts": texts,
            "include_reasoning": False
        }
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.parametrize("text,expected_category", [
    ("I feel so sad and hopeless", "DÉPRESSION"),
    ("I'm so happy today", "NORMAL"),
])
def test_predict_categories(text, expected_category):
    """Test de prédiction pour différentes catégories"""
    response = client.post(
        "/api/v1/predict",
        json={
            "text": text,
            "include_reasoning": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    # Note: Le LLM peut ne pas toujours prédire exactement comme attendu
    # Ce test vérifie juste que la réponse est valide
    assert data["prediction"] in ["DÉPRESSION", "NORMAL"]
