"""add_search_indexes

Revision ID: a6a22941b2a9
Revises: 5eeb073c04f6
Create Date: 2026-03-15 19:36:13.513770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6a22941b2a9'
down_revision: Union[str, Sequence[str], None] = '5eeb073c04f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    op.execute("CREATE INDEX IF NOT EXISTS idx_song_search_vector ON song USING GIN (search_vector)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_song_name_trgm ON song USING GIN (name gin_trgm_ops)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_song_artist_trgm ON song USING GIN (artist gin_trgm_ops)")

    op.execute("CREATE INDEX IF NOT EXISTS idx_userrecord_search_vector ON userrecord USING GIN (search_vector)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_userrecord_name_trgm ON userrecord USING GIN (name gin_trgm_ops)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_song_search_vector")
    op.execute("DROP INDEX IF EXISTS idx_song_name_trgm")
    op.execute("DROP INDEX IF EXISTS idx_song_artist_trgm")
    op.execute("DROP INDEX IF EXISTS idx_userrecord_search_vector")
    op.execute("DROP INDEX IF EXISTS idx_userrecord_name_trgm")
