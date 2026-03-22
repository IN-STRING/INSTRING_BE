import jwt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timedelta
from INewApp.core.dependencies import SessionDep
from INewApp.core.security.auth_mange import auth_manager
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.core.config import settings
from INewApp.domains.users.schemas.user_schemas import Tokens
from INewApp.core.redis_set import redis_client


LogInOut_router = APIRouter()


@LogInOut_router.post("/login")
async def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = auth_manager.check_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="입력 정보가 일치하지 않습니다")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_manager.create_token({"sub": str(user.id), "type": "access"}, access_token_expires)

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = jwt_manager.create_token({"sub": str(user.id), "type": "refresh"}, refresh_token_expires)

    redis_client.setex(
        f"refresh:{user.id}",
        settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        refresh_token
    )
    return Tokens(access_token=access_token, refresh_token=refresh_token, token_type="bearer")



@LogInOut_router.post("/logout")
async def logout(access_token: Annotated[str, Depends(jwt_manager.oauth2_scheme)]):
    payload = jwt.decode(access_token, settings.KEY, algorithms=["HS256"])
    user_id = payload["sub"]

    exp = payload["exp"]
    ttl = int(exp - datetime.utcnow().timestamp())
    if ttl > 0:
        redis_client.setex(f"blacklist:{access_token}", ttl, "logout")

    redis_client.delete(f"refresh:{user_id}")
    return {"message": "로그아웃 성공"}