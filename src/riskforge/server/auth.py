"""Bearer token authentication for the RiskForge API."""

from __future__ import annotations

import hashlib
import hmac

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> str:
    """Validate a Bearer token. Returns the token identity on success."""
    from riskforge.server.config import ServerConfig

    config = ServerConfig()
    token = credentials.credentials
    expected = hashlib.sha256((config.secret_key + ":api").encode()).hexdigest()

    if not hmac.compare_digest(token, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
