"""restore_user_record_search_vector

Revision ID: 736849a0839a
Revises: 0f4ba0861216
Create Date: 2026-03-11 21:14:38.973095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '736849a0839a'
down_revision: Union[str, Sequence[str], None] = '0f4ba0861216'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade():
    op.execute("""
        ALTER TABLE userrecord
        ADD COLUMN IF NOT EXISTS search_vector tsvector
        GENERATED ALWAYS AS (
            to_tsvector('simple', coalesce(name, ''))
        ) STORED;
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_userrecord_search_vector
        ON userrecord USING GIN (search_vector);
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_userrecord_name_trgm
        ON userrecord USING GIN (name gin_trgm_ops);
    """)

def downgrade():
    op.execute("DROP INDEX IF EXISTS idx_userrecord_name_trgm;")
    op.execute("DROP INDEX IF EXISTS idx_userrecord_search_vector;")
    op.execute("ALTER TABLE userrecord DROP COLUMN IF EXISTS search_vector;")