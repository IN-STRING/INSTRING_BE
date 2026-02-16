from jwt.exceptions import InvalidTokenError # 깔려 있음
import jwt
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from fastapi_mail import MessageSchema
from typing import Annotated
from datetime import timedelta
from app.api.depends import SessionDep, check_token
from app.core.config import fm, settings
from app.schemas.auth_dto import Email, Password, VerifyDTO, TempToken, RefreshToken
from app.models.redisDB.redis_set import redis_client
from app.models.postgresDB.user import User
from app.utils.auth_utils.email_cord import make_auth_otp
from app.utils.auth_utils.hash import hash_password
from app.core.security.jwt_token import create_token

change_router = APIRouter()


@change_router.post("/change_info_check")
async def check_email(email: Email):
    otp = make_auth_otp()
    redis_client.setex(f"verify:{email.email}", 300, otp)

    message = MessageSchema(
        subject="[INSTRING] 인증번호",
        recipients=[email.email],
        body=f"인증번호는 {otp} 입니다",
        subtype="html"
    )
    await fm.send_message(message)

    return {"Message" : "인증 코드가 성공적으로 발송 되었습니다."}


@change_router.post("/check_otp")
async def check_otp(data: VerifyDTO):
    code = redis_client.get(f"verify:{data.email}")
    if not code:
        raise HTTPException(status_code=404, detail="email not found")
    if code != data.otp:
        raise HTTPException(status_code=404, detail="code is wrong")
    redis_client.delete(f"verify:{data.email}")
    redis_client.setex(f"verified:{data.email}", 600, "true")

    temp_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    temp_token = create_token({"sub": data.email, "type": "temp"}, temp_token_expires)
    return TempToken(temp_token=temp_token, token_type="bearer")


@change_router.post("/change_password")
async def change_password(session: SessionDep, password: Password, userdata: Annotated[dict, Depends(check_token)]):
    stmt = select(User).where(User.email == userdata["sub"])
    user = session.exec(stmt).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if userdata["type"] != "temp":
        raise HTTPException(status_code=400, detail="이메일 인증 해라")

    user.password = hash_password(password.password)
    session.add(user)
    session.commit()
    return {"message": "변경 성공"}