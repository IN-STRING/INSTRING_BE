from sqlmodel import Field, SQLModel
from typing import Optional

class SongCategoryLink(SQLModel, table=True):
    song_id: Optional[int] = Field(default=None, foreign_key="song.id",primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id" ,primary_key=True)