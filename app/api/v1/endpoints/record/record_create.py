from fastapi import APIRouter, Depends
from typing import Annotated
from app.api.depends import SessionDep
from app.core.security.jwt_token import jwt_manager
from app.models.postgresDB.user_record import UserRecord
from app.schemas.record_dto import RecordCreateRequest
from app.services.AI_models.chord_model.chord_predict import Cpredictor
from app.services.AI_models.SAT_model.SAT_predict import FSpredictor

create_record_router = APIRouter()

@create_record_router.post("/record/create")
async def create_record(
        request: RecordCreateRequest,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)],
        session: SessionDep
):
    song_chord = Cpredictor.predict_result(request.file_url)
    song_style_speed = FSpredictor.analyze_guitar_performance(request.file_url)

    record = UserRecord(
        name=request.name,
        style=song_style_speed.style,
        chord=song_chord,
        speed=song_style_speed.tempo,
        file_url=request.file_url,
        spec_img_url=request.spec_img_url,
        user_id=userdata["sub"],
    )

    session.add(record)
    session.commit()
    session.refresh(record)
    return record