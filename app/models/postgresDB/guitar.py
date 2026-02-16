from sqlalchemy.orm import Mapped, relationship

from app.models.postgresDB.base import Base
from app.schemas.guitar_val import GuitarVal
# from app.models.postgresDB.user import User
from sqlmodel import Field, Relationship
from typing import Optional

class Guitar(Base, table=True):
    name: Optional[str] = Field(default=None)
    step: Optional[str] = Field(default=None)
    users: list["User"] = Relationship(back_populates="user_guitar")
    #users: Mapped["User"] = relationship("User", back_populates="user_guitar")