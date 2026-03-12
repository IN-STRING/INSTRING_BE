from fastapi import APIRouter
from app.api.v1.endpoints.auth.authentication import auth_router
from app.api.v1.endpoints.user_info.change_info import change_router
from app.api.v1.endpoints.user_info.modal import model_router
from app.api.v1.endpoints.infos.info_api import info_router
from app.api.v1.endpoints.device.socket.sensor_socket_api import socket_router
from app.api.v1.endpoints.device.socket.record_socket_api import record_socket_router
from app.api.v1.endpoints.user_info.user_info_api import user_info_router
from app.api.v1.endpoints.device.device_connection import device_router
from app.api.v1.endpoints.song_info.song_page import song_router
from app.api.v1.endpoints.search.search_songs.search_category import search_category_router
from app.api.v1.endpoints.search.search_songs.text_search import text_search_router
from app.api.v1.endpoints.record.record_create import create_record_router
from app.api.v1.endpoints.record.record_info import record_info_router
from app.api.v1.endpoints.record.record_change_info import record_change_info_router
from app.api.v1.endpoints.search.search_records.record_name_search import search_records_router
from app.api.v1.endpoints.user_info.user_song_click import user_song_click_router
from app.api.v1.endpoints.recommend.song_recommendation import song_recommendation_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(change_router, prefix="/change_info")
api_router.include_router(model_router, prefix="/model")
api_router.include_router(info_router, prefix="/category")
api_router.include_router(socket_router, prefix="/socket")
api_router.include_router(user_info_router, prefix="/level")
api_router.include_router(device_router, prefix="/device")
api_router.include_router(song_router, prefix="/song")
api_router.include_router(search_category_router, prefix="/search_category")
api_router.include_router(text_search_router, prefix="/text_search")
api_router.include_router(record_info_router, prefix="/record_info")
api_router.include_router(create_record_router, prefix="/create_record")
api_router.include_router(record_socket_router, prefix="/record_socket")
api_router.include_router(record_change_info_router, prefix="/record_change_info")
api_router.include_router(search_records_router, prefix="/record_search")
api_router.include_router(user_song_click_router, prefix="/user_song_click")
api_router.include_router(song_recommendation_router, prefix="/song_recommendation")