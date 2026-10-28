"""add games patch generated column

Revision ID: 78050a3de471
Revises: c6693b1cb401
Create Date: 2026-10-27 21:49:36.248026

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "78050a3de471"
down_revision: Union[str, None] = "c6693b1cb401"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "games",
        sa.Column(
            "patch",
            sa.Text(),
            sa.Computed(
                "split_part(game_version, '.', 1) || '.' || split_part(game_version, '.', 2)",
                persisted=True,
            ),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_games_patch_queue_id", "games", ["patch", "queue_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("idx_games_patch_queue_id", table_name="games")
    op.drop_column("games", "patch")
