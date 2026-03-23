from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from INewApp.common.base_model import Base
from INewApp.common.common_models.SongCategory_link import SongCategoryLink

if TYPE_CHECKING:
    from INewApp.domains.song.models.song import Song

class Category(Base, table=True):
    name: Optional[str] = Field(default=None)
    ctype: Optional[str] = Field(default=None)
    songs: list["Song"] = Relationship(back_populates="categories", link_model=SongCategoryLink)