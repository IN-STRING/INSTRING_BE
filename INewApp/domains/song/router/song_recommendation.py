from fastapi import APIRouter, Query
from INewApp.core.dependencies import SessionDep, CurrentUserId
from INewApp.domains.users.models.user_table import User
from INewApp.common.utils.song_repo_class import song_repository
from INewApp.domains.song.service.song_recommend import song_recommender

song_recommendation_router = APIRouter()


@song_recommendation_router.get("/song/recommend")
async def get_song_recommendation(
        session: SessionDep,
        userdata: CurrentUserId,
        limit: int = Query(default=12),
):
    user = await session.get(User, userdata["sub"])
    user_level = user.level_id
    user_history ,user_click = await song_repository.get_user_click_songs(session, userdata["sub"])

    result = await song_recommender.recommend(session, user_level ,user_history, user_click, limit)
    return {"recommend": result}