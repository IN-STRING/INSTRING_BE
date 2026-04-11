from fastapi import APIRouter
from sqlmodel import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from INewApp.core.config import settings
from INewApp.core.dependencies import SessionDep, CurrentUserId
from INewApp.domains.users.models.user_table import User

user_info_router = APIRouter()


@user_info_router.get("/user/level")
async def my_level(
        session: SessionDep,
        userdata: CurrentUserId
):
    result = await session.exec(
        select(User)
        .options(selectinload(User.user_level), selectinload(User.user_string))
        .where(User.id == int(userdata["sub"]))
    )
    user = result.first()
    level = user.user_level.id
    return {"level": level}


@user_info_router.get("/user/string-status")
async def get_string_status(
        session: SessionDep,
        userdata: CurrentUserId
):
    result = await session.exec(
        select(User)
        .options(selectinload(User.user_level), selectinload(User.user_string))
        .where(User.id == int(userdata["sub"]))
    )
    user = result.first()

    string_id = user.user_string.id
    changed_at = user.updated_at
    now = datetime.now(timezone.utc)
    elapsed = (now - changed_at).days

    progress = min(elapsed / settings.STRING_MAX_DAY, 1.0)

    if progress < 0.25:
        #message = "줄 상태가 좋습니다"
        status = "good"
    elif progress < 0.5:
        #message = "슬슬 교체를 고려해보세요"
        status = "normal"
    elif progress < 0.75:
        #message = "줄을 교체 하시는 것이 좋습니다!"
        status = "warning"
    else:
        #message = "악기줄이 너무 오래 되었습니다!!"
        status = "danger"

    return {
        "string_id": string_id,
        #"message": message,
        "status": status
    }