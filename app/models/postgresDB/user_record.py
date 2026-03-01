from sqlmodel import Field, Relationship
from typing import Optional
from app.models.postgresDB.base import Base
from app.models.postgresDB.user import User

class UserRecord(Base, table=True):
    name: str
    style: str
    chord: str
    speed: str
    spec_img_url: str
    file_url: str

    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    user_records: User = Relationship(back_populates="records")