from typing import Dict, Any
import docker
import logging

logger = logging.getLogger(__name__)

def check_docker_health() -> Dict[str, Any]:
    """Check Docker service health."""
    try:
        client = docker.from_env()
        client.ping()
        return {"status": "healthy", "message": "Docker service is running"}
    except Exception as e:
        logger.error(f"Docker health check failed: {e}")
        return {"status": "unhealthy", "message": str(e)}

def check_gpu_availability() -> Dict[str, Any]:
    """Check GPU availability."""
    try:
        client = docker.from_env()
        info = client.info()
        runtime = info.get("DefaultRuntime", "")
        has_gpu = "nvidia" in runtime or any(
            "nvidia" in r.get("Name", "").lower()
            for r in info.get("Runtimes", {}).values()
        )
        return {
            "status": "available" if has_gpu else "unavailable",
            "message": "GPU support detected" if has_gpu else "No GPU support detected"
        }
    except Exception as e:
        logger.error(f"GPU check failed: {e}")
        return {"status": "unknown", "message": str(e)}
