from jwt.exceptions import InvalidTokenError # 깔려 있음
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from fastapi_mail import MessageSchema
from typing import Annotated
from datetime import timedelta
from app.api.depends import SessionDep
from app.core.config import fm, settings
from app.schemas.auth_dto import Email, Password, VerifyDTO, TempToken
from app.models.redisDB.redis_set import redis_client
from app.models.postgresDB.user import User
from app.core.security.auth_mange import auth_manager
from app.core.security.jwt_token import jwt_manager

change_router = APIRouter()


@change_router.post("/change_info_check")
async def check_email(session: SessionDep, email: Email):
    stmt = select(User).where(User.email == email.email)
    result = session.exec(stmt).first()
    if not result:
        raise HTTPException(status_code=409, detail="가입되지 않은 이메일 입니다")

    otp = auth_manager.make_auth_otp()
    redis_client.setex(f"change_verify:{email.email}", 300, otp)

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
    code = redis_client.get(f"change_verify:{data.email}")
    if not code:
        raise HTTPException(status_code=404, detail="email not found")
    if code != data.otp:
        raise HTTPException(status_code=404, detail="code is wrong")
    redis_client.delete(f"change_verify:{data.email}")

    temp_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    temp_token = jwt_manager.create_token({"sub": data.email, "type": "temp"}, temp_token_expires)
    return TempToken(temp_token=temp_token, token_type="bearer")


@change_router.post("/change_password")
async def change_password(session: SessionDep, password: Password, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    stmt = select(User).where(User.email == userdata["sub"])
    user = session.exec(stmt).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if userdata["type"] != "temp":
        raise HTTPException(status_code=400, detail="이메일 인증 해라")

    user.password = auth_manager.hash_password(password.password)
    session.add(user)
    session.commit()
    return {"message": "변경 성공"}