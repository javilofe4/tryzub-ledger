from fastapi import Header, HTTPException

from ..core.config import settings


def get_admin_token(authorization: str | None = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing admin authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid admin token format")
    if not settings.ADMIN_TOKEN:
        raise HTTPException(status_code=503, detail="Admin token is not configured")
    token = authorization.split(" ", 1)[1]
    if token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return token
