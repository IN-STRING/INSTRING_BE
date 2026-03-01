from fastapi import APIRouter, Depends
from typing import Annotated
from app.api.depends import SessionDep
from app.models.postgresDB.user import User
from app.core.security.jwt_token import jwt_manager


user_info_router = APIRouter()

@user_info_router.get("/my_level")
async def my_level(session: SessionDep, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    user = session.get(User, userdata["sub"])
    level = user.user_level.id
    return {"level": level}


@user_info_router.get("/my_gstring")
async def my_gstring(session: SessionDep, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    user = session.get(User, userdata["sub"])
    result = user.user_gstring.id
    return {"gstring": result}