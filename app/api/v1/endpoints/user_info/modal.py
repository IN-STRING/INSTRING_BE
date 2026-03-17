from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from typing import Annotated
from app.core.security.jwt_token import jwt_manager
from app.api.depends import SessionDep
from app.schemas.modal_dto import ModalDTO
from app.models.postgresDB.level import Level
from app.models.postgresDB.g_string import GString
from app.models.postgresDB.user import User


model_router = APIRouter()


@model_router.get("/modal_check")
async def modal_bool(session: SessionDep, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    user = session.get(User, userdata["sub"])
    return user.modal

@model_router.post("/modal_add")
async def modal_add(session: SessionDep, modaldata: ModalDTO, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    user = session.get(User, userdata["sub"])
    if user.modal:
        raise HTTPException(status_code=400, detail="이미 완료함")

    result = session.exec(
        (
            select(GString, Level)
            .where(GString.name == modaldata.strings)
            .where(Level.name == modaldata.levels)
        )
    ).first()

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"선택한 정보를 DB에서 찾을 수 없습니다. (입력값: {modaldata.strings}, {modaldata.levels})"
        )

    gs, lv = result

    user.level_id = lv.id
    user.string_id = gs.id
    user.modal = modaldata.modal
    user.is_device = modaldata.device

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"Message": "success"}