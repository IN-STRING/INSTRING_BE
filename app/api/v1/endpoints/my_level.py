from fastapi import APIRouter, Depends
from typing import Annotated
from app.api.depends import SessionDep
from app.models.postgresDB.maintable.user import User
from app.core.security.jwt_token import jwt_manager


level_router = APIRouter()

@level_router.get("/my_level")
async def my_level(session: SessionDep, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    user = session.get(User, userdata["sub"])
    level = user.user_level.step
    return level