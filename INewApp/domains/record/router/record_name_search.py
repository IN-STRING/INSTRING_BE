from fastapi import APIRouter, Query, Depends
from typing import Annotated
from INewApp.domains.record.service.record_search import search_records
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.core.dependencies import SessionDep


search_records_router = APIRouter()


@search_records_router.get("/records/search")
def search(
    session: SessionDep,
    userdata: Annotated[dict, Depends(jwt_manager.check_token)],
    q: str = Query(..., min_length=1),
    limit: int = Query(20, le=50)
):
    results = search_records(session, q, userdata["sub"], limit)
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