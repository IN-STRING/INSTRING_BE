from fastapi import APIRouter, Query
from app.services.search_system.song_search import search_songs
from app.api.depends import SessionDep
from app.schemas.song_dto import SongS

text_search_router = APIRouter()

@text_search_router.get("/songs/search")
def search(
    session: SessionDep,
    q: str = Query(..., min_length=1),
    limit: int = Query(20, le=50),
):
    results = search_songs(session, q, limit)
    songs = {
        "songs":
                 [
                     SongS(
                         id=r.id,
                         name=r.name,
                         artist=r.artist,
                         level_id=r.level_id,
                         # style=r.style,
                         # speed=r.speed,
                         # chord=r.chord,
                     )
                     for r in results
                 ]
             }
    return songs