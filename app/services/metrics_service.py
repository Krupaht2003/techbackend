import psutil
from datetime import datetime, timedelta
from app.models.schemas import SystemMetrics
from app.utils.prometheus_metrics import CPU_USAGE, MEMORY_USAGE, DISK_USAGE
from app.utils.kubernetes_client import get_pod_count
import threading
import time

# In-memory storage for historical data (not persistent across restarts)
historical_data = []
data_lock = threading.Lock()  # Add a lock for thread safety

def get_current_metrics() -> SystemMetrics:
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # Update Prometheus metrics
    CPU_USAGE.set(cpu_percent)
    MEMORY_USAGE.set(memory.percent)
    DISK_USAGE.set(disk.percent)

    pod_count = get_pod_count()

    metrics = SystemMetrics(
        timestamp=datetime.now(),
        cpu_usage=cpu_percent,
        memory_usage=memory.percent,
        disk_usage=disk.percent,
        pod_count=pod_count
    )

    # Use lock when modifying the shared historical_data list
    with data_lock:
        historical_data.append(metrics)
        if len(historical_data) > 1000:
            historical_data.pop(0)

    return metrics

def get_historical_metrics(hours: int):
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    # Use lock when accessing the shared historical_data list
    with data_lock:
        # Filter metrics where timestamp is greater than cutoff time
        # No conversion needed since we're storing actual SystemMetrics objects
        return [metric for metric in historical_data if metric.timestamp > cutoff_time]

# Background task to collect metrics periodically
def collect_metrics_periodically(interval_seconds=60):
    while True:
        get_current_metrics()
        time.sleep(interval_seconds)

# Start the background collection when module is imported
metrics_thread = threading.Thread(target=collect_metrics_periodically, daemon=True)
metrics_thread.start()