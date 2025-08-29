from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any
import time
import logging
from .auth import get_api_key, rate_limiter, api_requests, request_duration
from .model_manager import ModelManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Docker Model Runner OpenAI-Compatible API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model manager
model_manager = ModelManager()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(256, gt=0)
    stream: Optional[bool] = False
    
class CompletionRequest(BaseModel):
    model: str
    prompt: str
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(256, gt=0)
    stream: Optional[bool] = False

class EmbeddingRequest(BaseModel):
    model: str
    input: Union[str, List[str]]
    encoding_format: Optional[str] = "float"

@app.post("/v1/chat/completions")
async def create_chat_completion(
    request: ChatCompletionRequest,
    api_key: str = Depends(get_api_key)
):
    """Create a chat completion."""
    rate_limiter.check(api_key)
    api_requests.labels(endpoint="chat_completions").inc()
    
    with request_duration.time():
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in request.messages
            ]
            
            response = model_manager.run_model(
                request.model,
                formatted_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return {
                "id": f"chatcmpl-{int(time.time()*1000)}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response["output"]
                    },
                    "finish_reason": "stop"
                }],
                "usage": response.get("usage", {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                })
            }
        except Exception as e:
            logger.error(f"Chat completion error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/completions")
async def create_completion(
    request: CompletionRequest,
    api_key: str = Depends(get_api_key)
):
    """Create a text completion."""
    rate_limiter.check(api_key)
    api_requests.labels(endpoint="completions").inc()
    
    with request_duration.time():
        try:
            response = model_manager.run_model(
                request.model,
                request.prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return {
                "id": f"cmpl-{int(time.time()*1000)}",
                "object": "text_completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [{
                    "text": response["output"],
                    "index": 0,
                    "finish_reason": "stop"
                }],
                "usage": response.get("usage", {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                })
            }
        except Exception as e:
            logger.error(f"Completion error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/embeddings")
async def create_embedding(
    request: EmbeddingRequest,
    api_key: str = Depends(get_api_key)
):
    """Create embeddings for text."""
    rate_limiter.check(api_key)
    api_requests.labels(endpoint="embeddings").inc()
    
    with request_duration.time():
        try:
            inputs = request.input if isinstance(request.input, list) else [request.input]
            
            response = model_manager.run_model(
                request.model,
                inputs
            )
            
            return {
                "object": "list",
                "data": [
                    {
                        "object": "embedding",
                        "embedding": emb,
                        "index": i
                    }
                    for i, emb in enumerate(response["embeddings"])
                ],
                "model": request.model,
                "usage": response.get("usage", {
                    "prompt_tokens": 0,
                    "total_tokens": 0
                })
            }
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def list_models(
    api_key: str = Depends(get_api_key)
):
    """List available models."""
    api_requests.labels(endpoint="models").inc()
    return model_manager.list_models()

@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics."""
    return Response(
        media_type="text/plain",
        content=generate_latest()
    )
