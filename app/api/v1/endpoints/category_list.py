from fastapi import APIRouter
from sqlmodel import select
from app.api.depends import SessionDep
from app.models.postgresDB.category import Category

category_router = APIRouter()

# 뭔가 오류 있음
@category_router.get("/categories")
async def get_categories(session: SessionDep):
    result = session.exec(select(Category.ctype)).all()
    return result