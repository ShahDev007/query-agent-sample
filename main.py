from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kubernetes import client, config
import logging
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str

app = FastAPI(title="Kubernetes Query Agent")

def init_kubernetes() -> bool:
    """Initialize Kubernetes configuration"""
    try:
        config.load_kube_config()
        logger.info("Successfully initialized Kubernetes configuration")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Kubernetes configuration: {e}")
        return False

def get_pod_deployment_relationship(pod_name: str) -> Optional[str]:
    """Find which deployment spawned a specific pod"""
    try:
        apps_v1 = client.AppsV1Api()
        deployments = apps_v1.list_deployment_for_all_namespaces()
        
        for deployment in deployments.items:
            if pod_name.startswith(deployment.metadata.name):
                return deployment.metadata.name
    except Exception as e:
        logger.error(f"Error finding deployment: {e}")
    return None

def get_pod_logs(pod_name: str, namespace: str = 'default') -> str:
    """Get logs for a specific pod"""
    try:
        v1 = client.CoreV1Api()
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        return logs if logs else "No logs available"
    except client.rest.ApiException as e:
        return f"Error getting logs: {e.reason}"


def process_query(query: str) -> str:
    """Process natural language queries about Kubernetes cluster"""
    query = query.lower().strip()
    try:
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()

        # Node queries
        if "how many nodes" in query:
            nodes = v1.list_node()
            return f"There are {len(nodes.items)} nodes in the cluster"

        # Pod status queries
        elif "status of pod" in query or "pod status" in query:
            pod_name = query.split("'")[1] if "'" in query else None
            if not pod_name:
                return "Please provide the pod name in quotes"
            pods = v1.list_pod_for_all_namespaces()
            for pod in pods.items:
                if pod.metadata.name == pod_name:
                    deployment = get_pod_deployment_relationship(pod.metadata.name)
                    return (
                        f"Pod '{pod.metadata.name}':\n"
                        f"Status: {pod.status.phase}\n"
                        f"Deployment: {deployment or 'Not found'}\n"
                        f"Namespace: {pod.metadata.namespace}"
                    )
            return f"Pod '{pod_name}' not found"

        # Deployment spawn queries - Fixed this section
        elif "deployment" in query and "pod" in query:  # Simplified condition
            try:
                pod_name = query.split("'")[1] if "'" in query else None
                if not pod_name:
                    return "Please provide the pod name in quotes"
                
                v1 = client.CoreV1Api()
                apps_v1 = client.AppsV1Api()
                
                try:
                    pod = v1.read_namespaced_pod(name=pod_name, namespace='default')
                    owner_refs = pod.metadata.owner_references
                    
                    if owner_refs:
                        rs_name = owner_refs[0].name
                        rs = apps_v1.read_namespaced_replica_set(name=rs_name, namespace='default')
                        deployment_name = rs.metadata.owner_references[0].name
                        return f"Pod '{pod_name}' was spawned by deployment '{deployment_name}'"
                    
                except client.rest.ApiException:
                    return f"Pod '{pod_name}' not found"
                    
            except Exception as e:
                logger.error(f"Error in deployment query: {e}")
                return f"Error finding deployment information: {str(e)}"

        # List deployments
        elif "deployments" in query:
            deployments = apps_v1.list_deployment_for_all_namespaces()
            return "Current deployments: " + ", ".join(
                d.metadata.name for d in deployments.items
            )

        else:
            return (
                "I understand queries about:\n"
                "- Number of nodes\n"
                "- Pod status (e.g., 'What is the status of pod 'nginx'')\n"
                "- Pod deployment relationship (e.g., 'Which deployment spawned pod 'nginx'')\n"
                "- List deployments"
            )

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    logger.info(f"Received query: {request.query}")
    answer = process_query(request.query)
    return QueryResponse(query=request.query, answer=answer)

@app.on_event("startup")
async def startup_event():
    if not init_kubernetes():
        logger.error("Failed to initialize Kubernetes configuration")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)