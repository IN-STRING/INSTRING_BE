from fastapi import APIRouter, Query
from INewApp.core.dependencies import SessionDep
from INewApp.common.common_models.category import Category
from INewApp.domains.song.schemas.song_dto import SearchCategory
from INewApp.domains.song.service.song_search import search_songs
from INewApp.domains.song.schemas.song_dto import SongS
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


search_router = APIRouter()


@search_router.get("/search/category/{ca_id}", response_model=SearchCategory)
async def get_ca(ca_id: int, session: SessionDep):
    result = await session.get(Category, ca_id)
    if result is None:
        raise AppException(ErrorCodes.CATEGORY_NOT_FOUND)
    return result


@search_router.get("/songs/search")
async def search(
    session: SessionDep,
    q: str = Query(..., min_length=1),
    limit: int = Query(20, le=50),
):
    results = await search_songs(session, q, limit)
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