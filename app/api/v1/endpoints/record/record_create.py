from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from app.api.depends import SessionDep
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.user_record import UserRecord
from app.schemas.record_dto import RecordCreateRequest

create_record_router = APIRouter()

@create_record_router.post("/record/create")
async def create_record(
        request: RecordCreateRequest,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)],
        session: SessionDep
):
    record = UserRecord(
        name=request.name,
        style=request.style,
        chord=request.chord,
        speed=request.speed,
        file_url=request.file_url,
        spec_img_url=request.spec_img_url,
        user_id=userdata["sub"],
    )

    session.add(record)
    session.commit()
    session.refresh(record)
    return record