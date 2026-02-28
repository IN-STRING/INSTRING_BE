from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.models.postgresDB.base import Base
from app.models.postgresDB.SongCategory_link import SongCategoryLink

if TYPE_CHECKING:
    from app.models.postgresDB.song import Song

class Category(Base, table=True):
    name: Optional[str] = Field(default=None)
    ctype: Optional[str] = Field(default=None)
    songs: list["Song"] = Relationship(back_populates="categories", link_model=SongCategoryLink)