from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import select
from app.api.depends import SessionDep
from app.models.postgresDB.song import Song
from app.models.postgresDB.user import User
from app.models.postgresDB.song_user_clicked_link import SongUserClickedLink
from app.core.security.jwt_token import jwt_manager
from app.services.song_repo.song_repo_class import song_repository
from app.services.reco_system.recommend import song_recommender

song_recommendation_router = APIRouter()


@song_recommendation_router.get("/song/recommend")
async def get_song_recommendation(
        session: SessionDep,
        userdata: Annotated[dict, Depends(jwt_manager.check_token())]
):
    pass