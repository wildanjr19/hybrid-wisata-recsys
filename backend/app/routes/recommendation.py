"""
API Routes untuk recommendation endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import (
    UserProfile, 
    RecommendationResponse, 
    WisataRecommendation,
    ErrorResponse
)
from app.services.recommendation_service import recommendation_service
from typing import List

# Create router
router = APIRouter()

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(user_profile: UserProfile, n: int = Query(5, ge=1, le=10)):
    """
    Generate rekomendasi wisata berdasarkan profil user
    
    Args:
        user_profile: Profil user (umur, asal_kota, jenis_kelamin)
        n: Jumlah rekomendasi (default 5, max 10)
    
    Returns:
        RecommendationResponse dengan list rekomendasi wisata
    """
    try:
        # Generate recommendations
        recommendations = recommendation_service.get_recommendations(
            umur=user_profile.umur,
            asal_kota=user_profile.asal_kota,
            jenis_kelamin=user_profile.jenis_kelamin,
            n_recommendations=n
        )
        
        # Convert to response model
        wisata_recommendations = [
            WisataRecommendation(**rec) for rec in recommendations
        ]
        
        return RecommendationResponse(
            user_profile=user_profile,
            recommendations=wisata_recommendations,
            total_recommendations=len(wisata_recommendations)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/wisata", response_model=List[WisataRecommendation])
async def get_all_wisata():
    """
    Get semua data wisata yang tersedia
    
    Returns:
        List of semua wisata
    """
    try:
        wisata_list = recommendation_service.get_all_wisata()
        return [WisataRecommendation(**w, score=0.0) for w in wisata_list]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/wisata/{wisata_id}", response_model=WisataRecommendation)
async def get_wisata_detail(wisata_id: str):
    """
    Get detail info untuk wisata tertentu
    
    Args:
        wisata_id: ID wisata (e.g., W1, W2, ...)
    
    Returns:
        Detail wisata
    """
    try:
        wisata_info = recommendation_service.get_wisata_info(wisata_id)
        if wisata_info is None:
            raise HTTPException(status_code=404, detail="Wisata not found")
        return WisataRecommendation(**wisata_info, score=0.0)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": recommendation_service.is_loaded,
        "total_wisata": len(recommendation_service.wisata_data) if recommendation_service.wisata_data is not None else 0
    }
