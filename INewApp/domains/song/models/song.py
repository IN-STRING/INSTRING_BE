from sqlmodel import Field, Relationship, Column, Integer, ForeignKey, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR
from typing import Optional, TYPE_CHECKING
from INewApp.common.base_model import Base
from INewApp.common.common_models.SongCategory_link import SongCategoryLink
from INewApp.common.common_models.song_user_clicked_link import SongUserClickedLink
from INewApp.common.common_models.category import Category
from INewApp.common.common_models.level import Level

if TYPE_CHECKING:
    from INewApp.common.common_models.level import Level
    from INewApp.common.common_models.category import Category
    from INewApp.domains.users.models.user_table import User

class Song(Base, table=True):
    name: str
    artist: str
    style: str
    speed: str
    # level_id: Optional[int] = Field(default=None, foreign_key="level.id", index=True)
    level_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("level.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )
    chord: str
    tube_url: str
    file_url: str

    categories: list[Category] = Relationship(back_populates="songs", link_model=SongCategoryLink)
    song_level: Optional[Level] = Relationship(back_populates="songs")

    clicked_users: list["User"] = Relationship(back_populates="clicked_songs", link_model=SongUserClickedLink)

    search_vector: Optional[str] = Field(
        default=None,
        sa_column=Column(
            TSVECTOR,
            Computed(
                "setweight(to_tsvector('simple', coalesce(name, '')), 'A') || "
                "setweight(to_tsvector('simple', coalesce(artist, '')), 'B')",
                persisted=True
            )
        )
    )