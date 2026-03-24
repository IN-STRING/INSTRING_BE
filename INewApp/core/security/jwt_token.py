import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, WebSocket
from typing import Annotated
from datetime import datetime, timedelta, timezone
from INewApp.core.redis_set import redis_client
from INewApp.core.config import settings


class JWTManager:
    def __init__(self):
        self.secret_key = settings.KEY
        self.algorithm = "HS256"
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
        self.credentials_exception = HTTPException(
            status_code=401,
            detail="토큰 검증 실패",
            headers={"WWW-Authenticate": "Bearer"}
        )

    def create_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def check_token(self, token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))]):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            if payload.get("type") not in ["access", "temp"]:
                raise self.credentials_exception

            if not payload.get("sub"):
                raise self.credentials_exception

            if redis_client.get(f"blacklist:{token}"):
                raise self.credentials_exception

            return payload

        except InvalidTokenError:
            raise self.credentials_exception

    async def check_token_ws(self, websocket: WebSocket):
        token = websocket.query_params.get("token")

        if not token:
            await websocket.close(code=1008, reason="Token missing")
            return None

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            if payload.get("type") not in ["access", "temp"]:
                await websocket.close(code=1008, reason="Invalid token")
                return None

            if not payload.get("sub"):
                await websocket.close(code=1008, reason="Invalid token")
                return None

            if redis_client.get(f"blacklist:{token}"):
                await websocket.close(code=1008, reason="Token revoked")
                return None

            return payload

        except InvalidTokenError:
            await websocket.close(code=1008, reason="Invalid token")
            return None

jwt_manager = JWTManager()