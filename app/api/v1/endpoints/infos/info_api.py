from fastapi import APIRouter
from sqlmodel import select
from app.api.depends import SessionDep
from app.models.postgresDB.category import Category
from app.models.postgresDB.level import Level
from app.models.postgresDB.guitar import Guitar
from app.models.postgresDB.g_string import GString

info_router = APIRouter()


@info_router.get("/categories")
async def get_categories(session: SessionDep):
    result = session.exec(select(Category)).all()
    return result


@info_router.get("/levels")
async def get_levels(session: SessionDep):
    result = session.exec(select(Level)).all()
    return result


@info_router.get("/guitars")
async def get_guitars(session: SessionDep):
    result = session.exec(select(Guitar)).all()
    return result


@info_router.get("/guitar_strings")
async def get_guitar_strings(session: SessionDep):
    result = session.exec(select(GString)).all()
    return result