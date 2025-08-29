from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import docker
import json

app = FastAPI(title="SmolLM2 OpenAI-Compatible API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Docker client
docker_client = docker.from_env()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 256

class CompletionRequest(BaseModel):
    model: str
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 256

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    try:
        # Format messages for the model
        formatted_messages = "\n".join([f"{msg.role}: {msg.content}" for msg in request.messages])
        
        # Run the model using Docker Model Runner
        container = docker_client.containers.run(
            "ai/smollm2",
            command=formatted_messages,
            remove=True,
            detach=False
        )
        
        response = container.decode('utf-8').strip()
        
        return {
            "id": "chatcmpl-" + docker_client.containers.run("alpine", "uuidgen", remove=True).decode('utf-8').strip(),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response
                },
                "finish_reason": "stop"
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/completions")
async def create_completion(request: CompletionRequest):
    try:
        # Run the model using Docker Model Runner
        container = docker_client.containers.run(
            "ai/smollm2",
            command=request.prompt,
            remove=True,
            detach=False
        )
        
        response = container.decode('utf-8').strip()
        
        return {
            "id": "cmpl-" + docker_client.containers.run("alpine", "uuidgen", remove=True).decode('utf-8').strip(),
            "object": "text_completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "text": response,
                "index": 0,
                "finish_reason": "stop"
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/models")
async def list_models():
    return {
        "data": [
            {
                "id": "ai/smollm2:360M-Q4_K_M",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "docker-model-runner",
                "permission": [],
                "root": "ai/smollm2",
                "parent": None
            }
        ]
    }
