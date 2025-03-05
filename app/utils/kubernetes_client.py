from kubernetes import client, config

def get_pod_count():
    try:
        config.load_incluster_config()
        k8s_client = client.CoreV1Api()
        return len(k8s_client.list_pod_for_all_namespaces().items)
    except:
        return 0
def check_kubernetes_health():
    try:
        config.load_incluster_config()
        k8s_client = client.CoreV1Api()
        k8s_client.list_node()  # Check if API is reachable
        return "healthy"
    except:
        return "unreachable"
def get_stateful_sets():
    try:
        config.load_incluster_config()
        k8s_client = client.AppsV1Api()
        stateful_sets = k8s_client.list_stateful_set_for_all_namespaces()
        return [{"name": ss.metadata.name, "replicas": ss.status.replicas} for ss in stateful_sets.items]
    except:
        return []
def get_daemon_sets():
    try:
        config.load_incluster_config()
        k8s_client = client.AppsV1Api()
        daemon_sets = k8s_client.list_daemon_set_for_all_namespaces()
        return [{"name": ds.metadata.name, "desired": ds.status.desired_number_scheduled, "current": ds.status.current_number_scheduled} for ds in daemon_sets.items]
    except:
        return []
def get_cluster_status():
    try:
        config.load_incluster_config()
        k8s_client = client.CoreV1Api()
        
        pod_count = len(k8s_client.list_pod_for_all_namespaces().items)
        node_count = len(k8s_client.list_node().items)
        
        return {"total_pods": pod_count, "total_nodes": node_count}
    except:
        return {"total_pods": 0, "total_nodes": 0}
def get_node_roles():
    try:
        config.load_incluster_config()
        k8s_client = client.CoreV1Api()
        nodes = k8s_client.list_node().items

        master_nodes = [node.metadata.name for node in nodes if "node-role.kubernetes.io/control-plane" in node.metadata.labels]
        worker_nodes = [node.metadata.name for node in nodes if "node-role.kubernetes.io/control-plane" not in node.metadata.labels]

        return {"master_nodes": len(master_nodes), "worker_nodes": len(worker_nodes)}
    except:
        return {"master_nodes": 0, "worker_nodes": 0}
