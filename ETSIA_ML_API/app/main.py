"""
Point d'entrée de l'application FastAPI - Architecture Multi-Modèles
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.routes import router
from app.models.schemas import HealthResponse
from app.core.model_registry import registry
from app.utils.logger import setup_logger
from datetime import datetime

logger = setup_logger(__name__)

# Créer l'application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION + " - Architecture Multi-Modèles",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Événement au démarrage - Enregistrement des modèles"""
    logger.info("="*70)
    logger.info(f"{settings.API_TITLE} v{settings.API_VERSION}")
    logger.info("Architecture Multi-Modèles")
    logger.info("="*70)
    
    # Enregistrer les modèles disponibles
    logger.info("\n📦 Enregistrement des modèles...")
    logger.info("-"*70)
    
    # 1. Modèle YANSNET LLM
    try:
        from app.services.yansnet_llm import YansnetLLMModel
        registry.register(YansnetLLMModel(), set_as_default=True)
    except Exception as e:
        logger.error(f"✗ Erreur lors de l'enregistrement du modèle YANSNET LLM: {e}")
        logger.error(f"  Vérifiez que .env est configuré avec les clés API")
    
    # 2. Autres modèles à ajouter ici
    # Exemple pour un futur étudiant:
    # try:
    #     from app.services.etudiant2_gcn import Etudiant2GCNModel
    #     registry.register(Etudiant2GCNModel())
    # except Exception as e:
    #     logger.error(f"✗ Erreur: {e}")
    
    # Résumé
    logger.info("-"*70)
    models = registry.list_models()
    if models:
        logger.info(f"✓ {len(models)} modèle(s) enregistré(s):")
        for name, info in models.items():
            default_marker = " [DÉFAUT]" if info.get('is_default') else ""
            logger.info(f"  • {name} v{info['version']} by {info['author']}{default_marker}")
    else:
        logger.warning("⚠️  Aucun modèle enregistré!")
    
    logger.info("="*70)
    logger.info("✓ API démarrée avec succès!")
    logger.info("📚 Documentation: http://localhost:8000/docs")
    logger.info("📋 Modèles disponibles: http://localhost:8000/api/v1/models")
    logger.info("="*70)


@app.on_event("shutdown")
async def shutdown_event():
    """Événement à l'arrêt"""
    logger.info("Arrêt de l'API...")


@app.get(
    "/",
    response_model=dict,
    summary="Page d'accueil",
    description="Informations sur l'API"
)
async def root():
    """Page d'accueil"""
    return {
        "message": "API de Détection de Dépression",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get(
    "/health",
    response_model=dict,
    summary="Health check",
    description="Vérifie l'état de l'API et des modèles"
)
async def health():
    """Health check global"""
    models_health = registry.health_check_all()
    models_list = registry.list_models()
    
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "models": {
            "total": len(models_list),
            "available": list(models_list.keys()),
            "health": models_health
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global pour les exceptions"""
    logger.error(f"Erreur non gérée: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erreur interne du serveur",
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )
