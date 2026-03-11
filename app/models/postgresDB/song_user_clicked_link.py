from sqlmodel import Field, SQLModel
from typing import Optional

class SongUserClickedLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id",primary_key=True)
    song_id: Optional[int] = Field(default=None, foreign_key="song.id" ,primary_key=True)
    click_count: int = Field(default=1)