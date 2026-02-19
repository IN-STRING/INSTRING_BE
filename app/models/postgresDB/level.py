from app.models.postgresDB.base import Base
from sqlmodel import Field, Relationship
from typing import Optional

class Level(Base, table=True):
    name: Optional[str] = Field(default=None)
    step: Optional[str] = Field(default=None)
    users: list["User"] = Relationship(back_populates="user_level")