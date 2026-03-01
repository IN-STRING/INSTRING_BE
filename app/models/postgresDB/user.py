from app.models.postgresDB.guitar import Guitar
from app.models.postgresDB.level import Level
from app.models.postgresDB.base import Base
from app.models.postgresDB.g_string import GString
from sqlmodel import Field, Relationship
from typing import Optional

class User(Base, table=True):
    email: str = Field(unique=True, index=True)
    password: str
    is_device: Optional[bool] = Field(default=False)
    modal: Optional[bool] = Field(default=False)
    device_id: Optional[str] = Field(default=None, unique=True, index=True)
    string_id: Optional[int] = Field(default=None, foreign_key="gstring.id", index=True)
    level_id: Optional[int] = Field(default=None, foreign_key="level.id", index=True)
    guitar_id: Optional[int] = Field(default=None, foreign_key="guitar.id", index=True)

    user_string: GString = Relationship(back_populates="users")
    user_level: Level = Relationship(back_populates="users")
    user_guitar: Guitar = Relationship(back_populates="users")

    records: list["User"] = Relationship(back_populates="user_records")