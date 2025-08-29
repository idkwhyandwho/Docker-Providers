@app.get("/health")
async def health_check():
    """Check the health of the API and its dependencies."""
    docker_health = check_docker_health()
    gpu_status = check_gpu_availability()
    
    health_status = {
        "status": "healthy" if docker_health["status"] == "healthy" else "unhealthy",
        "docker": docker_health,
        "gpu": gpu_status,
        "api_version": "1.0.0"
    }
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return Response(
        content=json.dumps(health_status),
        media_type="application/json",
        status_code=status_code
    )
