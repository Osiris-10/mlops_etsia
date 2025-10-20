#!/bin/bash

# Script de démarrage rapide pour l'API de détection de dépression

echo "=========================================="
echo "API de Détection de Dépression"
echo "=========================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✓ Python 3 détecté"

# Créer environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer dépendances
echo "📥 Installation des dépendances..."
pip install -q -r requirements.txt

# Vérifier .env
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "📝 Copie de .env.example vers .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Éditez le fichier .env avec vos clés API !"
    echo "   nano .env"
    echo ""
    read -p "Appuyez sur Entrée pour continuer..."
fi

# Lancer l'API
echo ""
echo "=========================================="
echo "🚀 Lancement de l'API..."
echo "=========================================="
echo ""
echo "📍 URL: http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""

uvicorn app.main:app --reload --port 8000
