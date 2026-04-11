from fastapi import APIRouter
from sqlalchemy.orm import selectinload
from sqlmodel import select
from INewApp.core.dependencies import SessionDep
from INewApp.domains.song.schemas.song_dto import WS
from INewApp.domains.song.models.song import Song
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes

song_router = APIRouter()

@song_router.get("/song/{song_id}", response_model=WS)
async def get_song(song_id: int, session: SessionDep):
    stmt = select(Song).where(Song.id == song_id).options(
        selectinload(Song.categories)
    )
    song = (await session.exec(stmt)).first()
    if song is None:
        raise AppException(ErrorCodes.SONG_NOT_FOUND)
    return song