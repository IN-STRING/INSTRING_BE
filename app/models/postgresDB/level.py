from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.postgresDB.base import Base

if TYPE_CHECKING:
    from app.models.postgresDB.song import Song
    from app.models.postgresDB.user import User

class Level(Base, table=True):
    name: Optional[str] = Field(default=None)
    step: Optional[str] = Field(default=None)
    users: list["User"] = Relationship(back_populates="user_level")
    songs: list["Song"] = Relationship(
        back_populates="song_level",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )