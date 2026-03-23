from fastapi import APIRouter, HTTPException, Query
from INewApp.core.dependencies import SessionDep
from INewApp.common.common_models.category import Category
from INewApp.domains.song.schemas.song_dto import SearchCategory
from INewApp.domains.song.service.song_search import search_songs
from INewApp.domains.song.schemas.song_dto import SongS


search_router = APIRouter()


@search_router.get("/search/category/{ca_id}", response_model=SearchCategory)
async def get_ca(ca_id: int, session: SessionDep):
    result = session.get(Category, ca_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return result


@search_router.get("/songs/search")
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