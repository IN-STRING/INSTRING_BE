from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.api.depends import SessionDep
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.maintable.user import User
from app.schemas.device_register import DeviceRegisterRequest


device_router = APIRouter()


# 프론트에서 여기로 접근
@device_router.post("/device/register")
async def register_device(
    body: DeviceRegisterRequest,
    session: SessionDep,
    userdata: Annotated[dict, Depends(jwt_manager.check_token)],
):
    user = session.get(User, userdata["sub"])

    if user.machinery_id:
        raise HTTPException(400, "이미 등록된 기기입니다")

    device = User(
        device_id=body.device_id
    )
    session.add(device)
    session.commit()

    return {"message": "기기 등록 완료", "device_id": body.device_id}