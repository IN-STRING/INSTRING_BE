from fastapi import APIRouter
from app.api.v1.endpoints.auth import auth_router
from app.api.v1.endpoints.change_info import change_router
from app.api.v1.endpoints.modal import model_router
from app.api.v1.endpoints.category_list import category_router
from app.api.v1.endpoints.websocket_api import socket_router
from app.api.v1.endpoints.my_level import level_router
from app.api.v1.endpoints.device import device_router

from app.models.postgresDB.song import Song
from app.models.postgresDB.user import User
from app.models.postgresDB.guitar import Guitar
from app.models.postgresDB.g_string import GString
from app.models.postgresDB.category import Category
from app.models.postgresDB.level import Level


api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(change_router, prefix="/change_info")
api_router.include_router(model_router, prefix="/model")
api_router.include_router(category_router, prefix="/category")
api_router.include_router(socket_router, prefix="/socket")
api_router.include_router(level_router, prefix="/level")
api_router.include_router(device_router, prefix="/device")