from sqlmodel import Field, Relationship
from typing import Optional
from app.models.postgresDB.base import Base

class Category(Base, table=True):
    name: Optional[str] = Field(default=None)
    ctype: Optional[str] = Field(default=None)
    # songs: list["Song"] = Relationship(back_populates="song_level")