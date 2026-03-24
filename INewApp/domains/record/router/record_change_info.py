from fastapi import APIRouter, Depends
from typing import Annotated
from INewApp.core.dependencies import SessionDep
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.domains.record.models.record_table import UserRecord
from INewApp.domains.record.schemas.record_schemas import ChangeRecord
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


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
        raise AppException(ErrorCodes.RECORD_NOT_FOUND)
    if record.user_id != int(userdata["sub"]):
        raise AppException(ErrorCodes.USER_NOT_FOUND)

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
        raise AppException(ErrorCodes.RECORD_NOT_FOUND)
    if record.user_id != int(userdata["sub"]):
        raise AppException(ErrorCodes.USER_NOT_FOUND)

    session.delete(record)
    session.commit()
    return {"Message": "파일이 성공적으로 삭제 되었습니다"}