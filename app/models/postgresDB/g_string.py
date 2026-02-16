from app.models.postgresDB.base import Base
from app.schemas.gstring_val import GStringEnum
#from app.models.postgresDB.user import User
from sqlmodel import Field, Relationship
from typing import Optional


class GString(Base, table=True):
    name: Optional[str] = Field(default=None)
    step: Optional[str] = Field(default=None)
    users: list["User"] = Relationship(back_populates="user_string")