from fastapi import FastAPI
from INewApp.core.middlewares import instring_middleware

from INewApp.domains.infos.info_api import info_router

from INewApp.domains.users.router.user_modal import model_router
from INewApp.domains.users.router.signup import signup_router
from INewApp.domains.users.router.song_click import user_song_click_router
from INewApp.domains.users.router.refresh import refresh_token_router
from INewApp.domains.users.router.patch_info import patch_user_router
from INewApp.domains.users.router.login import login_out_router
from INewApp.domains.users.router.get_user_info import user_info_router

from INewApp.domains.song.router.song_recommendation import song_recommendation_router
from INewApp.domains.song.router.song_page import song_router
from INewApp.domains.song.router.search_category import search_router
from INewApp.domains.song.router.song_contain import song_contain_router

from INewApp.domains.record.router.record_name_search import search_records_router
from INewApp.domains.record.router.record_info import record_info_router
from INewApp.domains.record.router.record_change_info import record_change_info_router

from INewApp.domains.device.router.device_connection import device_router
from INewApp.domains.device.socket.sensor_socket_api import sensor_socket
from INewApp.domains.device.socket.record_socket_api import device_socket_router
from INewApp.domains.device.socket.front_receive_socket_api import front_socket_router

from INewApp.core.error.exception_handlers import register_exception_handlers

app = FastAPI()


instring_middleware(app)

register_exception_handlers(app)

app.include_router(info_router)
app.include_router(signup_router)
app.include_router(model_router)
app.include_router(user_song_click_router)
app.include_router(refresh_token_router)
app.include_router(patch_user_router)
app.include_router(login_out_router, prefix="/auth")
app.include_router(user_info_router)
app.include_router(song_recommendation_router)
app.include_router(song_router)
app.include_router(song_contain_router)
app.include_router(search_router)
app.include_router(search_records_router)
app.include_router(record_info_router)
app.include_router(record_change_info_router)
app.include_router(device_router)
#app.include_router(sensor_socket)
app.include_router(device_socket_router)
app.include_router(front_socket_router)

# uvicorn INewApp.main:app --reload
# uvicorn INewApp.main:app --reload --host 0.0.0.0 --port 8000