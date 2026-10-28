"""add participant stats summary unique index

Revision ID: c6693b1cb401
Revises: 54e4856f81f8
Create Date: 2026-10-27 21:49:13.796302

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6693b1cb401"
down_revision: Union[str, None] = "54e4856f81f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    duplicates = (
        op.get_bind()
        .execute(
            sa.text(
                "SELECT count(*) FROM (SELECT participant_id FROM participant_stats "
                "WHERE game_time IS NULL GROUP BY participant_id HAVING count(*) > 1) d"
            )
        )
        .scalar()
    )
    if duplicates:
        raise RuntimeError(
            f"{duplicates} participants have more than one summary (game_time IS NULL) row"
        )
    with op.get_context().autocommit_block():
        # A failed concurrent build leaves an invalid index behind
        op.execute("DROP INDEX CONCURRENTLY IF EXISTS uq_participant_stats_summary")
        op.create_index(
            "uq_participant_stats_summary",
            "participant_stats",
            ["participant_id"],
            unique=True,
            postgresql_where=sa.text("game_time IS NULL"),
            postgresql_concurrently=True,
        )


def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.drop_index(
            "uq_participant_stats_summary",
            table_name="participant_stats",
            postgresql_concurrently=True,
        )
