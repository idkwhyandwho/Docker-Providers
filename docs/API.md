# API Documentation

## Authentication

All API requests require authentication using an API key. Include the key in the `Authorization` header:

```
Authorization: Bearer your-api-key
```

## Endpoints

### Chat Completions
`POST /v1/chat/completions`

Generate chat completions from messages.

Request:
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
}
```

### Text Completions
`POST /v1/completions`

Generate text completions from a prompt.

Request:
```json
{
    "model": "gpt-3.5-turbo",
    "prompt": "Once upon a time",
    "temperature": 0.7,
    "max_tokens": 150
}
```

### Embeddings
`POST /v1/embeddings`

Generate embeddings for text.

Request:
```json
{
    "model": "text-embedding-ada-002",
    "input": "Hello, world!"
}
```

### List Models
`GET /v1/models`

List available models.

## Error Handling

The API uses standard HTTP status codes:

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

Error responses include details:

```json
{
    "error": {
        "message": "Error description",
        "type": "error_type",
        "code": "error_code"
    }
}
```
