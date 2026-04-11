from fastapi import APIRouter, Query
from INewApp.domains.record.service.record_search import search_records
from INewApp.core.dependencies import SessionDep, CurrentUserId


search_records_router = APIRouter()


@search_records_router.get("/records/search")
async def search(
    session: SessionDep,
    userdata: CurrentUserId,
    q: str = Query(..., min_length=1),
    limit: int = Query(20, le=50)
):
    results = await search_records(session, q, int(userdata["sub"]), limit)
    return {
        "user_record":
            [
                {
                    "id": r.id,
                    "name": r.name,
                }
                for r in results
        ]
    }