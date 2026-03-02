from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from app.api.depends import SessionDep
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.user import User
from app.models.postgresDB.user_record import UserRecord

record_info_router = APIRouter()

@record_info_router.get("/record/info")
async def record_info(session: SessionDep, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    user = session.get(User, userdata["sub"])
    return user.records