from fastapi import APIRouter
from app.services.optimization_service import generate_optimization_recommendations
from app.models.schemas import OptimizationRecommendation
from typing import List

router = APIRouter()

@router.get("/recommendations", response_model=List[OptimizationRecommendation])
async def get_recommendations():
    """Get optimization recommendations"""
    return generate_optimization_recommendations()
