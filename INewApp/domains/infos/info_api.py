from fastapi import APIRouter
from sqlmodel import select
from INewApp.core.dependencies import SessionDep
from INewApp.common.common_models.category import Category
from INewApp.common.common_models.level import Level
from INewApp.domains.users.models.user_string import GString

info_router = APIRouter()


@info_router.get("/categories")
async def get_categories(session: SessionDep):
    result = await session.exec(select(Category))
    return {"categories": result.all()}


@info_router.get("/levels")
async def get_levels(session: SessionDep):
    result = await session.exec(select(Level))
    return {"levels": result.all()}


@info_router.get("/guitar_strings")
async def get_guitar_strings(session: SessionDep):
    result = await session.exec(select(GString))
    return {"strings": result.all()}