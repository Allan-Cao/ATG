"""Updates player table

Revision ID: ba9e31392997
Revises: 94f31f0160ad
Create Date: 2024-10-04 17:52:51.392111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba9e31392997'
down_revision: Union[str, None] = '94f31f0160ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('grid_id', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'players', ['grid_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'players', type_='unique')
    op.drop_column('players', 'grid_id')
    # ### end Alembic commands ###
