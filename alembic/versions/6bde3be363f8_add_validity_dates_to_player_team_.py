"""add validity dates to player team associations

Revision ID: 6bde3be363f8
Revises: 78050a3de471
Create Date: 2026-10-27 21:50:04.560975

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6bde3be363f8"
down_revision: Union[str, None] = "78050a3de471"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "player_team_associations", sa.Column("start_date", sa.Date(), nullable=True)
    )
    op.add_column(
        "player_team_associations", sa.Column("end_date", sa.Date(), nullable=True)
    )
    op.add_column(
        "player_team_associations",
        sa.Column(
            "updated", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.alter_column("player_team_associations", "updated", server_default=None)
    op.create_index(
        "uq_player_team_associations",
        "player_team_associations",
        ["player_id", "team_id", "position", "start_date"],
        unique=True,
        postgresql_nulls_not_distinct=True,
    )
    op.create_index(
        "idx_player_team_associations_team_id",
        "player_team_associations",
        ["team_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "idx_player_team_associations_team_id", table_name="player_team_associations"
    )
    op.drop_index("uq_player_team_associations", table_name="player_team_associations")
    op.drop_column("player_team_associations", "updated")
    op.drop_column("player_team_associations", "end_date")
    op.drop_column("player_team_associations", "start_date")
