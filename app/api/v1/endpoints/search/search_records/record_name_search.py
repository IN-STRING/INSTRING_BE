from fastapi import APIRouter, Query, Depends
from typing import Annotated
from app.services.search_system.record_search import search_records
from app.core.security.jwt_token import jwt_manager
from app.api.depends import SessionDep

search_records_router = APIRouter()

@search_records_router.get("/records/search")
def search(
    session: SessionDep,
    userdata: Annotated[dict, Depends(jwt_manager.check_token)],
    q: str = Query(..., min_length=1),
    limit: int = Query(20, le=50)
):
    user_id = userdata["sub"]
    results = search_records(session, q, user_id, limit)
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