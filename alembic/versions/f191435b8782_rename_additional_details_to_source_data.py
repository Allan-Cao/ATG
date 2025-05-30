"""Rename additional_details to source_data

Revision ID: f191435b8782
Revises: 8ba91bbca558
Create Date: 2025-05-29 21:43:56.407206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f191435b8782'
down_revision: Union[str, None] = '8ba91bbca558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("games", "additional_details", new_column_name="source_data")
    op.alter_column("tournaments", "additional_details", new_column_name="source_data")
    op.alter_column("game_events", "additional_details", new_column_name="source_data")


def downgrade() -> None:
    op.alter_column("games", "source_data", new_column_name="additional_details")
    op.alter_column("tournaments", "source_data", new_column_name="additional_details")
    op.alter_column("game_events", "source_data", new_column_name="additional_details")
