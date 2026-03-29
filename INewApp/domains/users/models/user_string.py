from INewApp.common.base_model import Base
from sqlmodel import Field, Relationship
from typing import Optional

# 너 enum으로 한다 테이블 삭제할거임
class GString(Base, table=True):
    name: Optional[str] = Field(default=None)
    step: Optional[str] = Field(default=None)
    users: list["User"] = Relationship(back_populates="user_string")