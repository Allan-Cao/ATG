"""Schema update

Revision ID: 8e791c9f409a
Revises: 
Create Date: 2025-02-07 17:34:42.791368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8e791c9f409a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('external_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.drop_column('players', 'associated_ids')
    op.add_column('teams', sa.Column('external_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.drop_constraint('teams_grid_id_key', 'teams', type_='unique')
    op.drop_constraint('teams_riot_esports_id_key', 'teams', type_='unique')
    op.drop_column('teams', 'grid_id')
    op.drop_column('teams', 'riot_esports_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('riot_esports_id', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('teams', sa.Column('grid_id', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_unique_constraint('teams_riot_esports_id_key', 'teams', ['riot_esports_id'])
    op.create_unique_constraint('teams_grid_id_key', 'teams', ['grid_id'])
    op.drop_column('teams', 'external_ids')
    op.add_column('players', sa.Column('associated_ids', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('players', 'external_ids')
    # ### end Alembic commands ###
