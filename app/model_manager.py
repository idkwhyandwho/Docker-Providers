import docker
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, config_path: str = "/app/config/config.json"):
        self.docker_client = docker.from_env()
        self.config = self._load_config(config_path)
        self.models = self.config.get("models", {})
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def run_model(
        self,
        model_name: str,
        input_data: Any,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Run a model using Docker container."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model_config = self.models[model_name]
        
        # Prepare container configuration
        container_config = {
            "image": model_config["image"],
            "command": json.dumps({
                "input": input_data,
                "parameters": {
                    "temperature": temperature or model_config.get("default_temperature", 0.7),
                    "max_tokens": max_tokens or model_config.get("max_tokens", 2048)
                }
            }),
            "volumes": {
                str(Path(model_config["model_path"]).parent): {
                    "bind": "/models",
                    "mode": "ro"
                }
            },
            "environment": {
                "CUDA_VISIBLE_DEVICES": "all"
            },
            "remove": True,
            "detach": False
        }
        
        try:
            container = self.docker_client.containers.run(**container_config)
            return json.loads(container.decode('utf-8'))
        except Exception as e:
            logger.error(f"Model execution failed: {e}")
            raise RuntimeError(f"Model execution failed: {str(e)}")
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        return {
            "id": model_name,
            "object": "model",
            "created": int(time.time()),
            "owned_by": "docker-model-runner",
            "permission": [],
            "root": model_name,
            "parent": None
        }
    
    def list_models(self) -> Dict[str, Any]:
        """List all available models."""
        return {
            "object": "list",
            "data": [
                self.get_model_info(model_name)
                for model_name in self.models
            ]
        }
