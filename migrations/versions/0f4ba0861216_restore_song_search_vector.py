"""restore_song_search_vector

Revision ID: 0f4ba0861216
Revises: 112e5489e801
Create Date: 2026-03-11 20:18:29.887406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = '0f4ba0861216'
down_revision: Union[str, Sequence[str], None] = '112e5489e801'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    op.execute("""
               ALTER TABLE song
                   ADD COLUMN IF NOT EXISTS search_vector tsvector
                   GENERATED ALWAYS AS (
                   setweight(to_tsvector('simple', coalesce (name, '')), 'A') ||
                   setweight(to_tsvector('simple', coalesce (artist, '')), 'B')
                   ) STORED;
               """)

    op.execute("""
               CREATE INDEX IF NOT EXISTS idx_song_search_vector
                   ON song USING GIN (search_vector);
               """)

    op.execute("""
               CREATE INDEX IF NOT EXISTS idx_song_name_trgm
                   ON song USING GIN (name gin_trgm_ops);
               """)
    op.execute("""
               CREATE INDEX IF NOT EXISTS idx_song_artist_trgm
                   ON song USING GIN (artist gin_trgm_ops);
               """)


def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_song_artist_trgm;")
    op.execute("DROP INDEX IF EXISTS idx_song_name_trgm;")
    op.execute("DROP INDEX IF EXISTS idx_song_search_vector;")
    op.execute("ALTER TABLE song DROP COLUMN IF EXISTS search_vector;")