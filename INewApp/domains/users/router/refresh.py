import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import APIRouter
from datetime import timedelta, datetime
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.core.config import settings
from INewApp.domains.users.schemas.user_schemas import RefreshToken, Tokens
from INewApp.core.redis_set import redis_client
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


refresh_token_router = APIRouter()


@refresh_token_router.post("/refresh")
async def get_access_token(token: RefreshToken):
    try:
        payload = jwt.decode(token.refresh_token, settings.KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise AppException(ErrorCodes.TOKEN_EXPIRED)
    except InvalidTokenError:
        raise AppException(ErrorCodes.INVALID_TOKEN)

    if payload["type"] != "refresh":
        raise AppException(ErrorCodes.WRONG_TOKEN)
    user_id = payload["sub"]
    saved_token = redis_client.get(f"refresh:{user_id}")
    if saved_token is None:
        raise AppException(ErrorCodes.WRONG_TOKEN)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_manager.create_token({"sub": str(user_id), "type": "access"}, access_token_expires)

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = jwt_manager.create_token({"sub": str(user_id), "type": "refresh"}, refresh_token_expires)

    # exp = payload["exp"]
    # ttl = int(exp - datetime.utcnow().timestamp())
    # if ttl > 0:
    #     redis_client.setex(f"blacklist:{saved_token}", ttl, "old_token")

    redis_client.setex(
        f"refresh:{user_id}",
        settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        refresh_token
    )
    return Tokens(access_token=access_token, refresh_token=refresh_token, token_type="bearer")