from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import Annotated
from app.api.depends import SessionDep
from app.services.ws.connect_socket import manager
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.user import User
from app.schemas.device_register import DeviceRegisterRequest


device_router = APIRouter()


@device_router.get("/device/check")
async def check_device(
        session: SessionDep,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)]
):
    user = session.get(User, userdata["sub"])
    return user.is_device


# 프론트에서 여기로 접근
@device_router.post("/device/register")
async def register_device(
    body: DeviceRegisterRequest,
    session: SessionDep,
    userdata: Annotated[dict, Depends(jwt_manager.check_token)],
):
    user = session.get(User, userdata["sub"])

    if user.device_id:
        raise HTTPException(400, "이미 등록된 기기입니다")

    if not manager.is_device_online(body.device_id):
        raise HTTPException(404, "기기를 찾을 수 없습니다")

    existing = session.exec(
        select(User).where(User.device_id == body.device_id)
    ).first()

    if existing:
        raise HTTPException(400, "이미 다른 사용자에게 등록된 기기입니다")

    user.device_id = body.device_id
    user.is_device = True

    session.add(user)
    session.commit()

    return {"message": "기기 등록 완료"}