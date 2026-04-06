from sqlmodel import select, Session, func
from INewApp.domains.song.models.song import Song
from INewApp.common.common_models.song_user_clicked_link import SongUserClickedLink


class SongRepository:

    @staticmethod
    def get_song_by_ids(session: Session, ids: list[int]):
        result = session.exec(select(Song).where(Song.id.in_(ids))).all()
        return result

    @staticmethod
    def get_songs_by_level(session: Session, level_id: int):
        result = session.exec(select(Song).where(Song.level_id == level_id)).all()
        return result

    @staticmethod
    def get_user_click_songs(session: Session, user_id: int):
        only_ids = []
        stmt = select(SongUserClickedLink).where(SongUserClickedLink.user_id == user_id)
        result = session.exec(stmt).all()

        for song in result:
            only_ids.append(song.song_id)

        return only_ids, result

    @staticmethod
    def get_all_click_counts(session: Session):
        stmt = (
            select(
                SongUserClickedLink.song_id,
                func.sum(SongUserClickedLink.click_count).label("total"),
            )
            .group_by(SongUserClickedLink.song_id)
        )
        rows = session.exec(stmt).all()
        return {song_id: int(total) for song_id, total in rows}


song_repository = SongRepository()