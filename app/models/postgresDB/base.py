from sqlmodel import SQLModel, Field, func, DateTime
from typing import Optional
from datetime import datetime, timezone

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

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

# uv run alembic revision --autogenerate -m "add_category_6"
# uv run alembic upgrade head