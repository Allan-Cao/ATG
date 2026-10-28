"""add accounts player_id index

Revision ID: 54e4856f81f8
Revises: 5db8f76d5748
Create Date: 2026-10-27 21:48:51.526135

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "54e4856f81f8"
down_revision: Union[str, None] = "5db8f76d5748"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("idx_accounts_player_id", "accounts", ["player_id"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_accounts_player_id", table_name="accounts")
