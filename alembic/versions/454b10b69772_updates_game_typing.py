"""Updates game typing

Revision ID: 454b10b69772
Revises: d35cbd5d03c0
Create Date: 2024-07-27 22:56:27.008433

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "454b10b69772"
down_revision: Union[str, None] = "d35cbd5d03c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("games", "game_id", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column(
        "games", "platform_id", existing_type=sa.VARCHAR(length=50), nullable=False
    )
    op.alter_column("games", "game_creation", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column("games", "game_start", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column("games", "game_end", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column(
        "games", "game_duration", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "games", "game_type", existing_type=sa.VARCHAR(length=50), nullable=False
    )
    op.alter_column(
        "games", "game_version_major", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "games", "game_version_minor", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "games", "game_version_minor", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "games", "game_version_major", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "games", "game_type", existing_type=sa.VARCHAR(length=50), nullable=True
    )
    op.alter_column("games", "game_duration", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("games", "game_end", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column("games", "game_start", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column("games", "game_creation", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column(
        "games", "platform_id", existing_type=sa.VARCHAR(length=50), nullable=True
    )
    op.alter_column("games", "game_id", existing_type=sa.BIGINT(), nullable=True)
    # ### end Alembic commands ###