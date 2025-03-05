from prometheus_client import Counter, Gauge, start_http_server

REQUESTS = Counter("resource_monitor_requests_total", "Total number of requests")
CPU_USAGE = Gauge("resource_monitor_cpu_usage", "Current CPU usage percentage")
MEMORY_USAGE = Gauge("resource_monitor_memory_usage", "Current memory usage percentage")
DISK_USAGE = Gauge("resource_monitor_disk_usage", "Current disk usage percentage")

start_http_server(8000)
