"""Rename foreign key champion to champion_id

Revision ID: 8ba91bbca558
Revises: 4490a7fa49d8
Create Date: 2025-05-26 20:58:30.064890

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8ba91bbca558"
down_revision: Union[str, None] = "4490a7fa49d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # For some reason the normal alter_table operation fails
    conn = op.get_bind()
    conn.execute(
        sa.sql.text(
            "ALTER TABLE IF EXISTS draft_events RENAME champion TO champion_id;"
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.sql.text(
            "ALTER TABLE IF EXISTS draft_events RENAME champion_id TO champion;"
        )
    )
