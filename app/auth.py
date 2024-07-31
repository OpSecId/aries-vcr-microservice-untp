from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from config import settings

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == settings.SECRET_KEY:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )
