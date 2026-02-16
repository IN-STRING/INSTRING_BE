import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from fastapi_mail import MessageSchema
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timedelta
from app.api.depends import SessionDep, oauth2_scheme
from app.core.config import fm, settings
from app.schemas.auth_dto import Email, UserJoinDTO, VerifyDTO, Tokens, RefreshToken, NewAccessToken
from app.models.redisDB.redis_set import redis_client
from app.models.postgresDB.user import User
from app.utils.auth_utils.email_cord import make_auth_otp
from app.utils.auth_utils.hash import hash_password
from app.utils.auth_utils.user_verfiy import check_user
from app.core.security.jwt_token import create_token

auth_router = APIRouter()


@auth_router.post("/email_check")
async def check_email(session: SessionDep, email: Email):
    stmt = select(User).where(User.email == email.email)
    result = session.exec(stmt).first()
    if result:
        raise HTTPException(status_code=409, detail="이미 가입된 이메일 입니다")

    otp = make_auth_otp()
    redis_client.setex(f"verify:{email.email}", 300, otp)

    message = MessageSchema(
        subject="[INSTRING] 회원가입 인증번호",
        recipients=[email.email],
        body=f"인증번호는 {otp} 입니다",
        subtype="html"
    )
    await fm.send_message(message)

    return {"Message" : "인증 코드가 성공적으로 발송 되었습니다."}



@auth_router.post("/check_otp")
async def check_otp(data: VerifyDTO):
    code = redis_client.get(f"verify:{data.email}")
    if not code:
        raise HTTPException(status_code=404, detail="email not found")
    if code != data.otp:
        raise HTTPException(status_code=404, detail="code is wrong")
    redis_client.delete(f"verify:{data.email}")
    redis_client.setex(f"verified:{data.email}", 600, "true")
    return {"message": "인증 성공!"}


@auth_router.post("/join")
async def login(session: SessionDep, userdata: UserJoinDTO ):
    try:
        result = redis_client.get(f"verify:{userdata.email}")
        if not result:
            raise HTTPException(status_code=404, detail="인증되지 않은 이메일 입니다")

        hashed_password = hash_password(userdata.password)
        dict_user = userdata.model_dump()
        dict_user["password"] = hashed_password
        db_user = User.model_validate(dict_user)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
        # return {"Message": "회원가입이 성공적으로 완료됬습니다"}

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="이미 가입된 이메일 입니다")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"서버 에러: {e}")


@auth_router.post("/login")
async def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = check_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="입력 정보가 일치하지 않습니다")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token({"sub": str(user.id), "type": "access"}, access_token_expires)

    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_token({"sub": str(user.id), "type": "refresh"}, refresh_token_expires)

    redis_client.setex(
        f"refresh:{user.id}",
        settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        refresh_token
    )
    return Tokens(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@auth_router.post("/refresh")
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
    access_token = create_token({"sub": str(user_id), "type": "access"}, access_token_expires)
    return NewAccessToken(access_token=access_token, token_type="bearer")


@auth_router.post("/logout")
async def logout(access_token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(access_token, settings.KEY, algorithms=["HS256"])
    user_id = payload["sub"]

    exp = payload["exp"]
    ttl = int(exp - datetime.utcnow().timestamp())
    if ttl > 0:
        redis_client.setex(f"blacklist:{access_token}", ttl, "logout")

    redis_client.delete(f"refresh:{user_id}")
    return {"message": "로그아웃 성공"}