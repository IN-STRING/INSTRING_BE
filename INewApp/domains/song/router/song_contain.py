import os
import tempfile
from typing import Annotated
from fastapi import APIRouter, File, UploadFile, Depends
from INewApp.core.dependencies import SessionDep
from INewApp.domains.song.schemas.song_dto import SongCreateRequest
from INewApp.domains.song.models.song import Song
from INewApp.domains.ai.SAT_model.SAT_predict import FSpredictor
from INewApp.domains.ai.chord_model.chord_predict import ChordPredictor


song_contain_router = APIRouter()


@song_contain_router.post("/song_contain")
async def song_contain(
    session: SessionDep,
    song: Annotated[SongCreateRequest, Depends(SongCreateRequest.as_form)],
    file: UploadFile = File(...)
):
    audio_bytes = await file.read()

    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        chords = ChordPredictor.predict_result(tmp_path)
        style_speed = FSpredictor.analyze_guitar_performance(tmp_path)

        song.chord = chords
        song.style = style_speed.style
        song.speed = style_speed.speed
        dict_song = song.model_dump()
        db_song = Song.model_validate(dict_song)

        session.add(db_song)
        session.commit()

    finally:
        os.remove(tmp_path)

    return {"message": "적제 완료"}