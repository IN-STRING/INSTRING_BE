from sqlmodel import select
from fastapi import APIRouter
from INewApp.core.dependencies import SessionDep, CurrentUserId
from INewApp.domains.users.schemas.modal import ModalDTO
from INewApp.common.common_models.level import Level
from INewApp.domains.users.models.user_string import GString
from INewApp.domains.users.models.user_table import User
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


model_router = APIRouter()


@model_router.get("/modal_check")
async def modal_bool(session: SessionDep, userdata: CurrentUserId):
    user = await session.get(User, userdata["sub"])
    return user.modal


@model_router.post("/modal_add")
async def modal_add(session: SessionDep, modaldata: ModalDTO, userdata: CurrentUserId):
    user = await session.get(User, userdata["sub"])
    if user.modal:
        raise AppException(ErrorCodes.MODAL_ALREADY_DONE)

    result = await session.exec(
        (
            select(GString, Level)
            .where(GString.name == modaldata.strings)
            .where(Level.name == modaldata.levels)
        )
    )
    info = result.first()

    if not info:
        raise AppException(ErrorCodes.WRONG_INFO)

    gs, lv = info

    user.level_id = lv.id
    user.string_id = gs.id
    user.modal = modaldata.modal
    user.is_device = modaldata.device

    session.add(user)
    return {"Message": "success"}