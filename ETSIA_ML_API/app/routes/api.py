"""
Routes API - Support multi-modèles
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from app.models.schemas import (
    PredictRequest,
    PredictResponse,
    BatchPredictRequest,
    BatchPredictResponse,
    ErrorResponse
)
from app.core.model_registry import registry
from app.utils.logger import setup_logger
import time

logger = setup_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Prédiction"])


@router.get(
    "/models",
    summary="Lister les modèles",
    description="Liste tous les modèles de détection disponibles"
)
async def list_models():
    """
    Liste tous les modèles disponibles avec leurs métadonnées.
    
    Retourne:
    - **models**: Dict des modèles avec leurs infos
    - **total**: Nombre total de modèles
    - **default**: Nom du modèle par défaut
    """
    models = registry.list_models()
    default_model = registry.get_default()
    
    return {
        "models": models,
        "total": len(models),
        "default": default_model.model_name if default_model else None
    }


@router.get(
    "/models/{model_name}/health",
    summary="Health check d'un modèle",
    description="Vérifie qu'un modèle spécifique est opérationnel"
)
async def model_health(model_name: str):
    """Vérifie la santé d'un modèle spécifique"""
    model = registry.get(model_name)
    if not model:
        raise HTTPException(
            status_code=404,
            detail=f"Modèle '{model_name}' non trouvé"
        )
    
    return model.health_check()


@router.post(
    "/predict",
    response_model=PredictResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Requête invalide"},
        404: {"model": ErrorResponse, "description": "Modèle non trouvé"},
        500: {"model": ErrorResponse, "description": "Erreur serveur"}
    },
    summary="Analyser un texte",
    description="Analyse un texte et détecte les signes de dépression avec le modèle spécifié"
)
async def predict(
    request: PredictRequest,
    model_name: Optional[str] = Query(
        None,
        description="Nom du modèle à utiliser (optionnel, utilise le défaut si non spécifié)"
    )
) -> PredictResponse:
    """
    Analyse un texte et détecte les signes de dépression.
    
    - **text**: Texte à analyser (1-5000 caractères)
    - **include_reasoning**: Inclure l'explication (défaut: true)
    - **model_name**: Modèle à utiliser (query param, optionnel)
    
    Retourne:
    - **prediction**: DÉPRESSION ou NORMAL
    - **confidence**: Niveau de confiance (0-1)
    - **severity**: Niveau de sévérité
    - **reasoning**: Explication (si demandé)
    - **model_used**: Nom du modèle utilisé
    """
    try:
        logger.info(f"Requête de prédiction (texte: {len(request.text)} chars, modèle: {model_name or 'default'})")
        
        # Récupérer le modèle
        if model_name:
            model = registry.get(model_name)
            if not model:
                available = registry.get_model_names()
                raise HTTPException(
                    status_code=404,
                    detail=f"Modèle '{model_name}' non trouvé. Disponibles: {available}"
                )
        else:
            model = registry.get_default()
            if not model:
                raise HTTPException(
                    status_code=500,
                    detail="Aucun modèle disponible. Vérifiez la configuration."
                )
        
        logger.info(f"  → Utilisation du modèle: {model.model_name}")
        
        # Prédire
        result = model.predict(
            text=request.text,
            include_reasoning=request.include_reasoning
        )
        
        # Construire la réponse
        return PredictResponse(
            prediction=result["prediction"],
            confidence=float(result["confidence"]),
            severity=result["severity"],
            reasoning=result.get("reasoning"),
            model_used=model.model_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de prédiction: {str(e)}"
        )


@router.post(
    "/batch-predict",
    response_model=BatchPredictResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Requête invalide"},
        404: {"model": ErrorResponse, "description": "Modèle non trouvé"},
        500: {"model": ErrorResponse, "description": "Erreur serveur"}
    },
    summary="Analyser plusieurs textes",
    description="Analyse plusieurs textes en batch (max 100)"
)
async def batch_predict(
    request: BatchPredictRequest,
    model_name: Optional[str] = Query(
        None,
        description="Nom du modèle à utiliser (optionnel)"
    )
) -> BatchPredictResponse:
    """
    Analyse plusieurs textes en batch.
    
    - **texts**: Liste de textes (1-100 textes)
    - **include_reasoning**: Inclure les explications (défaut: false)
    - **model_name**: Modèle à utiliser (query param, optionnel)
    
    Retourne:
    - **results**: Liste des prédictions
    - **total_processed**: Nombre de textes traités
    - **processing_time**: Temps de traitement (secondes)
    - **model_used**: Nom du modèle utilisé
    """
    try:
        logger.info(f"Requête batch ({len(request.texts)} textes, modèle: {model_name or 'default'})")
        
        # Récupérer le modèle
        if model_name:
            model = registry.get(model_name)
            if not model:
                available = registry.get_model_names()
                raise HTTPException(
                    status_code=404,
                    detail=f"Modèle '{model_name}' non trouvé. Disponibles: {available}"
                )
        else:
            model = registry.get_default()
            if not model:
                raise HTTPException(
                    status_code=500,
                    detail="Aucun modèle disponible"
                )
        
        logger.info(f"  → Utilisation du modèle: {model.model_name}")
        
        # Prédire
        start_time = time.time()
        results = model.batch_predict(
            texts=request.texts,
            include_reasoning=request.include_reasoning
        )
        processing_time = time.time() - start_time
        
        # Construire la réponse
        from app.models.schemas import BatchPredictResult
        
        formatted_results = []
        for i, (text, result) in enumerate(zip(request.texts, results)):
            formatted_results.append(BatchPredictResult(
                text=text[:100] + "..." if len(text) > 100 else text,
                prediction=result["prediction"],
                confidence=float(result["confidence"]),
                severity=result["severity"],
                reasoning=result.get("reasoning") if request.include_reasoning else None
            ))
        
        return BatchPredictResponse(
            results=formatted_results,
            total_processed=len(formatted_results),
            processing_time=round(processing_time, 2),
            model_used=model.model_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de prédiction batch: {str(e)}"
        )
