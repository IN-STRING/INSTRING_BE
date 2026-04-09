from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from INewApp.domains.song.models.song import Song
from INewApp.common.common_models.song_user_clicked_link import SongUserClickedLink


class SongRepository:

    @staticmethod
    async def get_song_by_ids(session: AsyncSession, ids: list[int]):
        result = session.exec(select(Song).where(Song.id.in_(ids))).all()
        return result

    @staticmethod
    async def get_songs_by_level(session: AsyncSession, level_id: int):
        result = await session.exec(select(Song).where(Song.level_id == level_id)).all()
        return result

    @staticmethod
    async def get_user_click_songs(session: AsyncSession, user_id: int):
        only_ids = []
        stmt = select(SongUserClickedLink).where(SongUserClickedLink.user_id == user_id)
        result = await session.exec(stmt).all()

        for song in result:
            only_ids.append(song.song_id)

        return only_ids, result

    @staticmethod
    async def get_all_click_counts(session: AsyncSession):
        stmt = (
            select(
                SongUserClickedLink.song_id,
                func.sum(SongUserClickedLink.click_count).label("total"),
            )
            .group_by(SongUserClickedLink.song_id)
        )
        rows = await session.exec(stmt).all()
        return {song_id: int(total) for song_id, total in rows}


song_repository = SongRepository()