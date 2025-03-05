import numpy as np
from app.models.schemas import OptimizationRecommendation
from app.services.metrics_service import historical_data, data_lock

def generate_optimization_recommendations():
    with data_lock:  # Use the lock when accessing historical_data
        if len(historical_data) < 10:
            return []

        recent_data = historical_data[-100:]
    
    # Process data outside the lock to minimize lock time
    cpu_values = [d.cpu_usage for d in recent_data]
    memory_values = [d.memory_usage for d in recent_data]

    avg_cpu = np.mean(cpu_values)
    max_cpu = np.max(cpu_values)
    avg_memory = np.mean(memory_values)
    max_memory = np.max(memory_values)

    recommendations = []

    if max_cpu < 50 and avg_cpu < 30:
        recommendations.append(OptimizationRecommendation(
            resource_type="cpu", 
            current_value=max_cpu, 
            recommended_value=max_cpu * 0.7, 
            reason="CPU underutilized", 
            potential_savings=30.0
        ))

    if max_memory < 50 and avg_memory < 30:
        recommendations.append(OptimizationRecommendation(
            resource_type="memory", 
            current_value=max_memory, 
            recommended_value=max_memory * 0.7, 
            reason="Memory underutilized", 
            potential_savings=30.0
        ))

    return recommendations