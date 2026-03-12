from sqlmodel import select, Session
from app.models.postgresDB.song import Song
from app.models.postgresDB.song_user_clicked_link import SongUserClickedLink

class SongRepository:
    def __init__(self):
        pass

    @staticmethod
    def get_song_by_ids(session: Session, ids: list[int]):
        result = session.exec(select(Song).where(Song.id.in_(ids))).all()
        return result

    @staticmethod
    def get_songs_by_level(session: Session, level_id: int):
        result = session.exec(select(Song).where(Song.level.id == level_id)).all()
        return result

    @staticmethod
    def get_user_click_songs(session: Session, user_id: int):
        only_ids = []
        stmt = select(SongUserClickedLink).where(SongUserClickedLink.user_id == user_id)
        result = session.exec(stmt).all()

        for song in result:
            only_ids.append(song.song_id)

        return result, only_ids

    @staticmethod
    def get_all_click_counts(session: Session):
        each_songs_total_count = dict()
        result = session.exec(select(SongUserClickedLink)).all()
        for song in result:
            if song.song_id in each_songs_total_count:
                each_songs_total_count[song.song_id] += song.click_count
            else:
                each_songs_total_count[song.song_id] = song.click_count
        return result


song_repository = SongRepository()