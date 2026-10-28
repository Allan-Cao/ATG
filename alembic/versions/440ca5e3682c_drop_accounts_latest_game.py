"""drop accounts latest_game

Revision ID: 440ca5e3682c
Revises: 6bde3be363f8
Create Date: 2026-10-27 21:50:17.410993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "440ca5e3682c"
down_revision: Union[str, None] = "6bde3be363f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("accounts", "latest_game")


def downgrade() -> None:
    op.add_column("accounts", sa.Column("latest_game", sa.BigInteger(), nullable=True))
