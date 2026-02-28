from fastapi import APIRouter
from app.api.depends import SessionDep
from app.models.postgresDB.category import Category
from app.schemas.category_dto import SearchCategory

search_category_router = APIRouter()

@search_category_router.get("/search/category/{ca_id}", response_model=SearchCategory)
async def get_ca(ca_id: int, session: SessionDep):
    result = session.get(Category, ca_id)
    return result
