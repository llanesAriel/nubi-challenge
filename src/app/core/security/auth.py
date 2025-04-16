from app.core.config import settings
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME, auto_error=False)


async def validate_api_key(api_key: str = Security(api_key_header)):
    print(api_key, settings.API_KEY)
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o faltante.",
        )
