"""Changes to game table

Revision ID: db637245a08b
Revises: e0d2bbbb17aa
Create Date: 2024-07-28 04:17:18.759276

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "db637245a08b"
down_revision: Union[str, None] = "e0d2bbbb17aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("games", sa.Column("patch", sa.String(length=10), nullable=True))
    op.add_column(
        "games", sa.Column("tournament_id", sa.String(length=50), nullable=True)
    )
    op.add_column("games", sa.Column("game_number", sa.Integer(), nullable=True))
    op.add_column("games", sa.Column("update", sa.DateTime(), nullable=True))
    op.alter_column("games", "game_creation", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column("games", "game_start", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column("games", "game_end", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column("games", "game_duration", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column(
        "games", "game_type", existing_type=sa.VARCHAR(length=50), nullable=True
    )
    op.create_foreign_key(None, "games", "tournaments", ["tournament_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "games", type_="foreignkey")
    op.alter_column(
        "games", "game_type", existing_type=sa.VARCHAR(length=50), nullable=False
    )
    op.alter_column(
        "games", "game_duration", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column("games", "game_end", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column("games", "game_start", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column("games", "game_creation", existing_type=sa.BIGINT(), nullable=False)
    op.drop_column("games", "update")
    op.drop_column("games", "game_number")
    op.drop_column("games", "tournament_id")
    op.drop_column("games", "patch")
    # ### end Alembic commands ###