from fastapi import APIRouter
from app.services.metrics_service import get_current_metrics, get_historical_metrics
from app.models.schemas import SystemMetrics
from typing import List
from app.utils.kubernetes_client import get_stateful_sets

router = APIRouter()

@router.get("/current", response_model=SystemMetrics)
async def get_metrics():
    """Get current system metrics"""
    return get_current_metrics()

# @router.get("/historical", response_model=List[SystemMetrics])
# def get_historical_metrics(hours: int = 1):
#     """Get historical metrics"""
#     return get_historical_metrics(hours)
@router.get("/historical", response_model=List[SystemMetrics])
async def historical_metrics(hours: int = 1):
    """Get historical metrics"""
    return get_historical_metrics(hours)

@router.get("/statefulsets")
async def stateful_sets():
    """Get details of all StatefulSets"""
    return get_stateful_sets()
from app.utils.kubernetes_client import get_daemon_sets

@router.get("/daemonsets")
async def daemon_sets():
    """Get details of all DaemonSets"""
    return get_daemon_sets()

from app.utils.kubernetes_client import get_cluster_status

@router.get("/cluster-status")
async def cluster_status():
    """Get total number of pods and nodes"""
    return get_cluster_status()

from app.utils.kubernetes_client import get_node_roles

@router.get("/node-roles")
async def node_roles():
    """Get number of master and worker nodes"""
    return get_node_roles()
