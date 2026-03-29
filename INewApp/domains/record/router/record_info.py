from fastapi import APIRouter, Depends, Query
from typing import Annotated
from sqlmodel import select
from INewApp.core.dependencies import SessionDep
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.domains.record.schemas.record_schemas import SearchRecords
from INewApp.domains.record.models.record_table import UserRecord
from INewApp.domains.record.service.record_recommend import record_recommender
from INewApp.domains.users.models.user_table import User
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


record_info_router = APIRouter()


@record_info_router.get("/record/list", response_model=SearchRecords)
async def record_info(
        session: SessionDep,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)]
):
    stmt = select(UserRecord).where(UserRecord.user_id == userdata["sub"])
    records = session.exec(stmt).all()
    return {"records": records}


@record_info_router.get("/record/info/{record_id}")
async def record_info(
        session: SessionDep,
        record_id: int,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)],
        limit: int = Query(default=12),
):
    record = session.get(UserRecord, record_id)
    user = session.get(User, userdata["sub"])
    if not record:
        raise AppException(ErrorCodes.RECORD_NOT_FOUND)
    if record.user_id != int(userdata["sub"]):
        raise AppException(ErrorCodes.USER_NOT_FOUND)

    analysis = {
        "style": record.style,
        "tempo": record.speed,
        "chords": record.chord,
    }

    results = record_recommender.recommend(session, user_level=user.level_id, analysis=analysis, limit=limit)

    return {"record_info": record, "recommend": results}