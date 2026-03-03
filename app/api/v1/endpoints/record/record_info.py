from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.api.depends import SessionDep
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.user import User
from app.models.postgresDB.user_record import UserRecord

record_info_router = APIRouter()

@record_info_router.get("/record/list")
async def record_info(session: SessionDep, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    user = session.get(User, userdata["sub"])
    return user.records

@record_info_router.get("/record/info/{record_id}")
async def record_info(
        session: SessionDep,
        record_id: int,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)]
):
    record = session.get(UserRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != int(userdata["sub"]):
        raise HTTPException(status_code=403, detail="User not found")

    return record