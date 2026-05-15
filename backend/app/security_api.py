"""API-ключ для write-операций (как в MetLab12)."""

from hmac import compare_digest

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config import Settings, get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(
    provided_key: str | None = Security(api_key_header),
    settings: Settings = Depends(get_settings),
) -> None:
    if provided_key is None or not compare_digest(provided_key, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
