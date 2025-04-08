from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader


API_KEY = "secret123"
api_key_header = APIKeyHeader(name="Authorization")


def get_current_user(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
