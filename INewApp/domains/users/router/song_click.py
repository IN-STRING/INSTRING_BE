from fastapi import APIRouter
from sqlmodel import select
from INewApp.core.dependencies import SessionDep, CurrentUserId
from INewApp.domains.song.models.song import Song
from INewApp.common.common_models.song_user_clicked_link import SongUserClickedLink
from INewApp.core.error.exceptions import AppException
from INewApp.core.error.exception_messages import ErrorCodes


user_song_click_router = APIRouter()


@user_song_click_router.get("/user/song/click/{song_id}")
async def user_song_click(
        song_id: int,
        session: SessionDep,
        userdata: CurrentUserId
):
    song = await session.get(Song, song_id)
    if not song:
        raise AppException(ErrorCodes.SONG_NOT_FOUND)

    result = await session.exec(
        select(SongUserClickedLink).where(
            SongUserClickedLink.song_id == song_id,
            SongUserClickedLink.user_id == int(userdata["sub"])
        )
    )
    is_song = result.first()

    if is_song:
        is_song.click_count += 1
    else:
        click_song = SongUserClickedLink(song_id=song_id, user_id=int(userdata["sub"]))
        session.add(click_song)

    return {"message": "클릭 기록 추가됨"}