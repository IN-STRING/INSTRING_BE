from fastapi import APIRouter
from INewApp.core.dependencies import SessionDep, CurrentUserId
from INewApp.domains.record.models.record_table import UserRecord
from INewApp.domains.record.schemas.record_schemas import ChangeRecord
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


record_change_info_router = APIRouter()


@record_change_info_router.patch("/record/change/info/{record_id}")
async def record_change_name(
        session: SessionDep,
        record_id: int,
        change_info: ChangeRecord,
        userdata: CurrentUserId
):
    record = await session.get(UserRecord, record_id)
    if not record:
        raise AppException(ErrorCodes.RECORD_NOT_FOUND)
    if record.user_id != int(userdata["sub"]):
        raise AppException(ErrorCodes.USER_NOT_FOUND)

    record.name = change_info.name

    session.add(record)
    return {"message": "이름 변경 성공"}


@record_change_info_router.delete("/record/delete/info/{record_id}")
async def record_delete(
        session: SessionDep,
        record_id: int,
        userdata: CurrentUserId
):
    record = await session.get(UserRecord, record_id)
    if not record:
        raise AppException(ErrorCodes.RECORD_NOT_FOUND)
    if record.user_id != int(userdata["sub"]):
        raise AppException(ErrorCodes.USER_NOT_FOUND)

    session.delete(record)
    return {"Message": "파일이 성공적으로 삭제 되었습니다"}