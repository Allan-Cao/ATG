"""Add debug timestamp to tournament

Revision ID: ba40f60cb515
Revises: ec4c0b65e4c2
Create Date: 2025-03-05 23:58:29.874233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'ba40f60cb515'
down_revision: Union[str, None] = 'ec4c0b65e4c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournaments', sa.Column('updated', sa.DateTime(), nullable=False, server_default=str(datetime.now())))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournaments', 'updated')
    # ### end Alembic commands ###
