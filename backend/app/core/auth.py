from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    """
    Middleware to verify API key for secure endpoints.
    Can be toggled via API_KEY_REQUIRED in settings.
    """
    if not settings.API_KEY_REQUIRED:
        return True  # Skip in development or if disabled
    
    if not api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header missing")
        
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
        
    return True
