from app.core.db_engine import engine
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import settings
from app.models.redisDB.redis_set import redis_client

def get_session():
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def check_token(token: Annotated[str, Depends(oauth2_scheme)]):
    token_incorrect = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.KEY, algorithms=["HS256"])
        if payload["type"] not in ["access", "temp"]:
            raise token_incorrect
        userdata = payload.get("sub")
        if userdata is None:
            raise token_incorrect
        black = redis_client.get(f"blacklist:{token}")
        if black:
            raise token_incorrect
    except InvalidTokenError:
        raise token_incorrect
    return payload