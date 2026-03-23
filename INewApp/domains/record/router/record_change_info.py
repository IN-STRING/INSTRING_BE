from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from INewApp.core.dependencies import SessionDep
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.domains.record.models.record_table import UserRecord
from INewApp.domains.record.schemas.record_schemas import ChangeRecord


record_change_info_router = APIRouter()


@record_change_info_router.patch("/record/change/info/{record_id}")
async def record_change_info(
        session: SessionDep,
        record_id: int,
        change_info: ChangeRecord,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)]
):
    record = session.get(UserRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != int(userdata["sub"]):
        raise HTTPException(status_code=403, detail="User not found")

    record.name = change_info.name

    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@record_change_info_router.delete("/record/delete/info/{record_id}")
async def record_change_info(
        session: SessionDep,
        record_id: int,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)]
):
    record = session.get(UserRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    if record.user_id != int(userdata["sub"]):
        raise HTTPException(status_code=403, detail="User not found")

    session.delete(record)
    session.commit()
    return {"Message": "파일이 성공적으로 삭제 되었습니다"}