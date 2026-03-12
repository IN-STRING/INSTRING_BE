from fastapi import APIRouter, Depends, Query
from typing import Annotated
from app.api.depends import SessionDep
from app.models.postgresDB.user import User
from app.core.security.jwt_token import jwt_manager
from app.services.song_repo.song_repo_class import song_repository
from app.services.reco_system.recommend import song_recommender

song_recommendation_router = APIRouter()


@song_recommendation_router.get("/song/recommend")
async def get_song_recommendation(
        session: SessionDep,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)],
        limit: int = Query(default=12),
):
    user_level = session.get(User, userdata["sub"]).level_id
    user_history ,user_click = song_repository.get_user_click_songs(session, userdata["sub"])

    result = song_recommender.recommend(session, user_level ,user_history, user_click, limit)
    return result