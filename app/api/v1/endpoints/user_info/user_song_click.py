from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import select
from app.api.depends import SessionDep
from app.models.postgresDB.song import Song
from app.models.postgresDB.song_user_clicked_link import SongUserClickedLink
from app.core.security.jwt_token import jwt_manager

user_song_click_router = APIRouter()

@user_song_click_router.post("/user/song/click/{song_id}")
async def user_song_click(
        song_id: int,
        session: SessionDep,
        userdata: Annotated[dict, Depends(jwt_manager.check_token)]
):
    song = session.get(Song, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    is_song = session.exec(
        select(SongUserClickedLink).where(
            SongUserClickedLink.song_id == song_id,
            SongUserClickedLink.user_id == userdata["sub"]
        )
    ).first()

    if is_song:
        is_song.click_count += 1
    else:
        click_song = SongUserClickedLink(song_id=song_id, user_id=userdata["sub"])
        session.add(click_song)

    session.commit()
    return {"message": "클릭 기록 추가됨"}


@user_song_click_router.get("/user/song/click")
async def user_song_click_get(session: SessionDep, userdata: Annotated[dict, Depends(jwt_manager.check_token)]):
    only_ids = []
    stmt = select(SongUserClickedLink).where(SongUserClickedLink.user_id == userdata["sub"])
    result = session.exec(stmt).all()

    for song in result:
        only_ids.append(song.song_id)

    return result, only_ids