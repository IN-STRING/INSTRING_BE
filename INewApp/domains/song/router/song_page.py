from fastapi import APIRouter, HTTPException
from INewApp.core.dependencies import SessionDep
from INewApp.domains.song.schemas.song_dto import WS
from INewApp.domains.song.models.song import Song

song_router = APIRouter()

@song_router.get("/song{song_id}", response_model=WS)
async def get_song(song_id: int, session: SessionDep):
    result = session.get(Song, song_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return result