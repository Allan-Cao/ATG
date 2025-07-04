"""add team_stat table

Revision ID: 7b0a1b0e60ca
Revises: 0d7df9b7995e
Create Date: 2025-07-03 15:10:35.729966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b0a1b0e60ca'
down_revision: Union[str, None] = '0d7df9b7995e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team_stats',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('game_id', sa.Text(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('game_time', sa.Integer(), nullable=False),
    sa.Column('deaths', sa.Integer(), nullable=False),
    sa.Column('assists', sa.Integer(), nullable=False),
    sa.Column('champion_kills', sa.Integer(), nullable=False),
    sa.Column('total_gold', sa.Integer(), nullable=False),
    sa.Column('baron_kills', sa.Integer(), nullable=False),
    sa.Column('inhib_kills', sa.Integer(), nullable=False),
    sa.Column('tower_kills', sa.Integer(), nullable=False),
    sa.Column('dragon_kills', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_stats')
    # ### end Alembic commands ###
