from sqlmodel import select, Session
from app.api.depends import SessionDep
from app.models.postgresDB.user import User
from app.models.postgresDB.song import Song


def recommend_song(session: Session, user_id: int):
    user = session.get(User, user_id)
    level = user.level.id

