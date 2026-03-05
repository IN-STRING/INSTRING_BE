from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware

from app.models.postgresDB.song import Song
from app.models.postgresDB.user import User
from app.models.postgresDB.guitar import Guitar
from app.models.postgresDB.g_string import GString
from app.models.postgresDB.category import Category
from app.models.postgresDB.level import Level


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 나중에 프론트 url 추가
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")