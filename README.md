---
title: Docker-Providers
emoji: 🐳
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---

# Docker-Providers

This project provides an OpenAI-compatible API interface for running the SmolLM2 model using Docker Model Runner. It allows you to use SmolLM2 as a drop-in replacement for OpenAI's API, making it easy to integrate with existing applications.

## Features

- OpenAI-compatible API endpoints
- Support for both chat completions and text completions
- Docker Model Runner integration with SmolLM2
- Easy deployment with Docker

## Prerequisites

- Docker
- Docker Model Runner
- Python 3.11+

## Getting Started

1. Pull the SmolLM2 model:
```bash
docker model pull ai/smollm2
```

2. Build and run the API:
```bash
# Build the Docker image
docker build -t smollm2-api .

# Run the container
docker run -d -p 8000:8000 --name smollm2-api smollm2-api
```

## API Endpoints

### Chat Completions
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Text Completions
```bash
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "prompt": "Once upon a time"
  }'
```

### List Models
```bash
curl http://localhost:8000/v1/models
```

## Model Information

SmolLM2-360M is a compact language model with 360 million parameters, designed for:
- Chat assistants
- Text-extraction
- Rewriting and summarization

Available variants:
- ai/smollm2:360M-Q4_K_M (default)
- ai/smollm2:135M-Q4_0
- ai/smollm2:135M-Q4_K_M
- ai/smollm2:135M-F16
- ai/smollm2:135M-Q2_K
- ai/smollm2:360M-Q4_0
- ai/smollm2:360M-F16

## License

This project is licensed under the Apache 2.0 License.