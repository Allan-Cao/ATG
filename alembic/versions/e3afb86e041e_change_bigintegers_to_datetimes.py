"""Change bigintegers to datetimes

Revision ID: e3afb86e041e
Revises: 0ca0b0f9cb59
Create Date: 2025-05-31 21:34:51.501155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3afb86e041e'
down_revision: Union[str, None] = '0ca0b0f9cb59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE games 
        ALTER COLUMN game_creation TYPE TIMESTAMP WITH TIME ZONE 
        USING to_timestamp(game_creation / 1000.0)
    """)
    
    op.execute("""
        ALTER TABLE games 
        ALTER COLUMN game_end_timestamp TYPE TIMESTAMP WITH TIME ZONE 
        USING to_timestamp(game_end_timestamp / 1000.0)
    """)
    
    op.execute("""
        ALTER TABLE games 
        ALTER COLUMN game_start_timestamp TYPE TIMESTAMP WITH TIME ZONE 
        USING to_timestamp(game_start_timestamp / 1000.0)
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE games 
        ALTER COLUMN game_start_timestamp TYPE BIGINT 
        USING EXTRACT(EPOCH FROM game_start_timestamp)::BIGINT * 1000
    """)
    
    op.execute("""
        ALTER TABLE games 
        ALTER COLUMN game_end_timestamp TYPE BIGINT 
        USING EXTRACT(EPOCH FROM game_end_timestamp)::BIGINT * 1000
    """)
    
    op.execute("""
        ALTER TABLE games 
        ALTER COLUMN game_creation TYPE BIGINT 
        USING EXTRACT(EPOCH FROM game_creation)::BIGINT * 1000
    """)