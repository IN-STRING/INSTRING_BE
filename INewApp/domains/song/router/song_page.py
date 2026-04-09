from fastapi import APIRouter
from INewApp.core.dependencies import SessionDep
from INewApp.domains.song.schemas.song_dto import WS
from INewApp.domains.song.models.song import Song
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes

song_router = APIRouter()

@song_router.get("/song/{song_id}", response_model=WS)
async def get_song(song_id: int, session: SessionDep):
    result = await session.get(Song, song_id)
    if result is None:
        raise AppException(ErrorCodes.SONG_NOT_FOUND)
    return result