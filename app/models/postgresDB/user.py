from app.models.postgresDB.level import Level
from app.models.postgresDB.base import Base
from app.models.postgresDB.g_string import GString
from app.models.postgresDB.song_user_clicked_link import SongUserClickedLink
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.postgresDB.song import Song
    from app.models.postgresDB.user_record import UserRecord

class User(Base, table=True):
    email: str = Field(unique=True, index=True)
    password: str
    is_device: Optional[bool] = Field(default=False)
    modal: Optional[bool] = Field(default=False)
    device_id: Optional[str] = Field(default=None, unique=True, index=True)
    string_id: Optional[int] = Field(default=None, foreign_key="gstring.id", index=True)
    level_id: Optional[int] = Field(default=None, foreign_key="level.id", index=True)

    user_string: GString = Relationship(back_populates="users")
    user_level: Level = Relationship(back_populates="users")

    records: list["UserRecord"] = Relationship(
        back_populates="user_records",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )

    clicked_songs: list["Song"] = Relationship(back_populates="clicked_users", link_model=SongUserClickedLink)