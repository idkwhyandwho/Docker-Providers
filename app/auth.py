from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import time
from typing import Optional
from prometheus_client import Counter, Histogram

# Initialize security scheme
security = HTTPBearer()

# Metrics
api_requests = Counter('api_requests_total', 'Total API requests', ['endpoint'])
request_duration = Histogram('request_duration_seconds', 'Request duration in seconds')

def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Validate API key from Bearer token."""
    expected_key = os.getenv("API_KEY", "sk-default-key")
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing API key")
    
    if credentials.credentials != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return credentials.credentials

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = []
    
    def check(self, api_key: str) -> bool:
        """Check if request is within rate limits."""
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Remove old requests
        self.requests = [req for req in self.requests if req > minute_ago]
        
        if len(self.requests) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again in a minute."
            )
        
        self.requests.append(current_time)
        return True

rate_limiter = RateLimiter()
