from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SystemMetrics(BaseModel):
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    pod_count: int

class OptimizationRecommendation(BaseModel):
    resource_type: str
    current_value: float
    recommended_value: float
    reason: str
    potential_savings: Optional[float] = None
