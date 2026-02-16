import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from app.core.config import settings

def create_token(data: dict, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, settings.KEY, algorithm="HS256")
    return encoded_jwt