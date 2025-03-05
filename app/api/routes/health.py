from fastapi import APIRouter
from app.utils.kubernetes_client import check_kubernetes_health

router = APIRouter()

@router.get("/")
async def health_check():
     """Health check endpoint"""
     kubernetes_status = check_kubernetes_health()
     return {"status": "healthy", "kubernetes": kubernetes_status}