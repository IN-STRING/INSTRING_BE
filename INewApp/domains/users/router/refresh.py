import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, HTTPException
from datetime import timedelta
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.core.config import settings
from INewApp.domains.users.schemas.user_schemas import RefreshToken, NewAccessToken
from INewApp.core.redis_set import redis_client


refresh_token_router = APIRouter()


@refresh_token_router.post("/refresh")
async def get_access_token(token: RefreshToken):
    try:
        payload = jwt.decode(token.refresh_token, settings.KEY, algorithms=["HS256"])
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="not refresh token")
        user_id = payload["sub"]
        saved_token = redis_client.get(f"refresh:{user_id}")
        if saved_token is None:
            raise HTTPException(status_code=401, detail="not refresh token")

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="not token")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_manager.create_token({"sub": str(user_id), "type": "access"}, access_token_expires)
    return NewAccessToken(access_token=access_token, token_type="bearer")