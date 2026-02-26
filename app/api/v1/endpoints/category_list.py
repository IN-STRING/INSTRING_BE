from fastapi import APIRouter
from sqlmodel import select
from app.api.depends import SessionDep
from app.models.postgresDB.metatable.category import Category

category_router = APIRouter()

@category_router.get("/categories")
async def get_categories(session: SessionDep):
    result = session.exec(select(Category.ctype)).all()
    return result