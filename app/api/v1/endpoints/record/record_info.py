from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from sqlmodel import select
from app.api.depends import SessionDep
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.user import User
from app.schemas.record_dto import SearchRecords
from app.models.postgresDB.user_record import UserRecord
from app.services.reco_system.record_recommend import record_recommender

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
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != int(userdata["sub"]):
        raise HTTPException(status_code=403, detail="User not found")

    analysis = {
        "style": record.style,
        "tempo": record.speed,
        "chords": record.chord,
    }

    results = record_recommender.recommend(session, user_level=13, analysis=analysis, limit=limit)

    return {"record_info": record, "recommend": results}