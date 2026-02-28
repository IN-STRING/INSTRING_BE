from fastapi import APIRouter
from app.api.v1.endpoints.auth import auth_router
from app.api.v1.endpoints.user_info.change_info import change_router
from app.api.v1.endpoints.user_info.modal import model_router
from app.api.v1.endpoints.infos.info_api import info_router
from app.api.v1.endpoints.device.websocket_api import socket_router
from app.api.v1.endpoints.user_info.my_level import level_router
from app.api.v1.endpoints.device.device_connection import device_router
from app.api.v1.endpoints.song_info.song_page import song_router
from app.api.v1.endpoints.search.search_category import search_category_router
from app.api.v1.endpoints.search.text_search import text_search_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(change_router, prefix="/change_info")
api_router.include_router(model_router, prefix="/model")
api_router.include_router(info_router, prefix="/category")
api_router.include_router(socket_router, prefix="/socket")
api_router.include_router(level_router, prefix="/level")
api_router.include_router(device_router, prefix="/device")
api_router.include_router(song_router, prefix="/song")
api_router.include_router(search_category_router, prefix="/search_category")
api_router.include_router(text_search_router, prefix="/text_search")