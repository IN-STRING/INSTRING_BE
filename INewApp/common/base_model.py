from sqlmodel import SQLModel, Field, func, DateTime
from typing import Optional
from datetime import datetime
from INewApp.common.utils import  utcnow


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=utcnow,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "nullable": False,
            "server_default": func.now(),
        },
    )
    updated_at: datetime = Field(
        default_factory=utcnow,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={
            "nullable": False,
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )


class Base(TimestampMixin):
    id: Optional[int] = Field(default=None, primary_key=True)