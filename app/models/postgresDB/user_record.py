from sqlmodel import Field, Relationship, Column, Integer, ForeignKey, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR
from typing import Optional, TYPE_CHECKING
from app.models.postgresDB.base import Base
from app.models.postgresDB.user import User

if TYPE_CHECKING:
    from app.models.postgresDB.user import User

class UserRecord(Base, table=True):
    name: str
    style: Optional[str] = Field(default=None)
    chord: Optional[str] = Field(default=None)
    speed: Optional[str] = Field(default=None)
    spec_img_url: str
    file_url: str

    #user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    user_id: Optional[int] = Field(
        sa_column=Column(
            Integer,
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
            default=None
        )
    )
    user_records: User = Relationship(back_populates="records")

    search_vector: Optional[str] = Field(
        default=None,
        sa_column=Column(
            TSVECTOR,
            Computed(
                "to_tsvector('simple', coalesce(name, ''))",
                persisted=True
            )
        )
    )