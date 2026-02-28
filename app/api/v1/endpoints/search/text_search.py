# routers/song.py
from fastapi import APIRouter, Query
from app.services.search_system.fts_pg_tgrm_search import search_songs
from app.api.depends import SessionDep

text_search_router = APIRouter()

@text_search_router.get("/songs/search")
def search(
    session: SessionDep, q: str = Query(..., min_length=1),
    limit: int = Query(20, le=50),
):
    results = search_songs(session, q, limit)
    return [
        {
            "id": r.id,
            "name": r.name,
            "artist": r.artist,
            "style": r.style,
            # "speed": r.speed,
            # "chord": r.chord,
            "fts_score": r.fts_score,
            "trgm_score": r.trgm_score,
        }
        for r in results
    ]