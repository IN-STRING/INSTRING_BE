from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from fastapi_mail import MessageSchema
from INewApp.core.dependencies import SessionDep
from INewApp.core.security.auth_mange import auth_manager
from INewApp.core.config import fm
from INewApp.domains.users.schemas.user_schemas import Email, UserJoinDTO, VerifyDTO
from INewApp.core.redis_set import redis_client
from INewApp.domains.users.models.user_table import User
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


signup_router = APIRouter()


@signup_router.post("/email_check")
async def check_email(session: SessionDep, email: Email):
    stmt = select(User).where(User.email == email.email)
    result = session.exec(stmt).first()
    if result:
        raise AppException(ErrorCodes.USER_ALREADY_EXISTS)

    otp = auth_manager.make_auth_otp()
    redis_client.setex(f"verify:{email.email}", 300, otp)

    message = MessageSchema(
        subject="[INSTRING] 회원가입 인증번호",
        recipients=[email.email],
        body=f"인증번호는 {otp} 입니다",
        subtype="html"
    )
    await fm.send_message(message)

    return {"Message" : "인증 코드가 성공적으로 발송 되었습니다."}



@signup_router.post("/check_otp")
async def check_otp(data: VerifyDTO):
    code = redis_client.get(f"verify:{data.email}")
    if not code:
        raise AppException(ErrorCodes.FAILED)
    if code != data.otp:
        raise AppException(ErrorCodes.CODE_WRONG)
    redis_client.delete(f"verify:{data.email}")
    redis_client.setex(f"verified:{data.email}", 600, "true")
    return {"message": "인증 성공!"}



@signup_router.post("/join", status_code=HTTPStatus.CREATED)
async def login(session: SessionDep, userdata: UserJoinDTO ):
    try:
        result = redis_client.get(f"verified:{userdata.email}")
        if not result:
            raise AppException(ErrorCodes.EMAIL_FORBIDDEN)

        hashed_password = auth_manager.hash_password(userdata.password)
        dict_user = userdata.model_dump()
        dict_user["password"] = hashed_password
        db_user = User.model_validate(dict_user)

        session.add(db_user)
        session.commit()

        return {"Message": "회원가입이 성공적으로 완료됬습니다"}

    except IntegrityError as e:
        session.rollback()
        print("IntegrityError:", e)
        print("orig:", e.orig)
        raise AppException(ErrorCodes.USER_ALREADY_EXISTS)