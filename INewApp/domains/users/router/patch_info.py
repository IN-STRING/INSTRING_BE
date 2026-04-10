from fastapi import APIRouter
from sqlmodel import select
from fastapi_mail import MessageSchema
from datetime import timedelta
from INewApp.core.dependencies import SessionDep, CurrentUserId
from INewApp.core.security.auth_mange import auth_manager
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.core.config import fm
from INewApp.domains.users.schemas.user_schemas import Email, VerifyDTO, Password, TempToken
from INewApp.core.redis_set import redis_client
from INewApp.common.common_models.level import Level
from INewApp.domains.users.models.user_table import User
from INewApp.domains.users.models.user_string import GString
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


patch_user_router = APIRouter()


@patch_user_router.post("/change_info_check")
async def check_email(session: SessionDep, email: Email):
    stmt = select(User).where(User.email == email.email)
    result = await session.exec(stmt)
    user = result.first()
    if not user:
        raise AppException(ErrorCodes.USER_EMAIL_NOT_FOUND)

    # otp = auth_manager.make_auth_otp()
    # redis_client.setex(f"change_verify:{email.email}", 300, otp)
    #
    # message = MessageSchema(
    #     subject="[INSTRING] 인증번호",
    #     recipients=[email.email],
    #     body=f"인증번호는 {otp} 입니다",
    #     subtype="html"
    # )
    # await fm.send_message(message)
    await auth_manager.send_otp(email.email, prefix="change_verify")

    return {"Message" : "인증 코드가 성공적으로 발송 되었습니다."}


@patch_user_router.post("/change/check_otp")
async def check_otp(data: VerifyDTO):
    code = await redis_client.get(f"change_verify:{data.email}")
    if not code:
        raise AppException(ErrorCodes.FAILED)
    if code != data.otp:
        raise AppException(ErrorCodes.CODE_WRONG)
    redis_client.delete(f"change_verify:{data.email}")

    temp_token_expires = timedelta(minutes=5)
    temp_token = jwt_manager.create_token({"sub": data.email, "type": "temp"}, temp_token_expires)
    return TempToken(temp_token=temp_token, token_type="bearer")


@patch_user_router.patch("/change_password")
async def change_password(
        session: SessionDep,
        password: Password,
        userdata: CurrentUserId
):
    if userdata["type"] != "temp":
        raise AppException(ErrorCodes.EMAIL_FORBIDDEN)
    stmt = select(User).where(User.email == userdata["sub"])
    result = await session.exec(stmt)
    user = result.first()
    if not user:
        raise AppException(ErrorCodes.USER_NOT_FOUND)

    user.password = auth_manager.hash_password(password.password)
    session.add(user)
    return {"message": "변경 성공"}


@patch_user_router.patch("/change_level")
async def change_level(
        session: SessionDep,
        level_id: int,
        userdata: CurrentUserId
):
    level = await session.get(Level, level_id)
    if not level:
        raise AppException(ErrorCodes.LEVEL_NOT_FOUND)
    user = await session.get(User, userdata["sub"])
    user.level_id = level_id

    session.add(user)
    return {"message": "success"}


@patch_user_router.patch("/change_string")
async def change_string(
        session: SessionDep,
        string_id: int,
        userdata: CurrentUserId
):
    string = await session.get(GString, string_id)
    if not string:
        raise AppException(ErrorCodes.STRING_NOT_FOUND)
    user = await session.get(User, userdata["sub"])
    user.string_id = string_id

    session.add(user)
    return {"message": "success"}


@patch_user_router.delete("/user_delete")
async def withdraw(
    session: SessionDep,
    userdata: CurrentUserId
):
    user = await session.get(User, userdata["sub"])

    session.delete(user)
    return {"message": "success"}