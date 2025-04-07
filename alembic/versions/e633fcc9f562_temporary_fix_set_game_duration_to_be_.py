"""Temporary fix set game_duration to be nullable

Revision ID: e633fcc9f562
Revises: d410813554f6
Create Date: 2025-04-06 22:25:45.683251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e633fcc9f562'
down_revision: Union[str, None] = 'd410813554f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('participants', 'game_duration',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade() -> None:
    op.alter_column('participants', 'game_duration',
               existing_type=sa.INTEGER(),
               nullable=False)
