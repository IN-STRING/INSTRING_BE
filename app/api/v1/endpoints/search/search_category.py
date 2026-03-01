from fastapi import APIRouter, HTTPException
from app.api.depends import SessionDep
from app.models.postgresDB.category import Category
from app.schemas.category_dto import SearchCategory

search_category_router = APIRouter()

@search_category_router.get("/search/category/{ca_id}", response_model=SearchCategory)
async def get_ca(ca_id: int, session: SessionDep):
    result = session.get(Category, ca_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return result
