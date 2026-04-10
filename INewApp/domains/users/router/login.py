import jwt
from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from INewApp.core.dependencies import SessionDep
from INewApp.core.security.auth_mange import auth_manager
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.core.config import settings
from INewApp.domains.users.schemas.user_schemas import Tokens, UserJoinDTO
from INewApp.core.redis_set import redis_client
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes



login_out_router = APIRouter()


@login_out_router.post("/login")
async def login(
        session: SessionDep,
        #data: Annotated[OAuth2PasswordRequestForm, Depends()],
        data: UserJoinDTO
):
    user = await auth_manager.check_user(session, data.email, data.password)
    #user = auth_manager.check_user(session, data.username, data.password)
    if not user:
        raise AppException(ErrorCodes.WRONG_INFO)

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



@login_out_router.post("/logout")
async def logout(access_token: Annotated[str, Depends(jwt_manager.oauth2_scheme)]):
    payload = jwt.decode(access_token, settings.KEY, algorithms=["HS256"])
    user_id = payload["sub"]

    exp = payload["exp"]
    ttl = int(exp - datetime.now(timezone.utc).timestamp())
    if ttl > 0:
        redis_client.setex(f"blacklist:{access_token}", ttl, "logout")

    redis_client.delete(f"refresh:{user_id}")
    return {"message": "로그아웃 성공"}