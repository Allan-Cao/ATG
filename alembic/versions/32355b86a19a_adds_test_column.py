"""Adds test column

Revision ID: 32355b86a19a
Revises: b90b0154f05c
Create Date: 2024-10-12 15:45:43.179208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32355b86a19a'
down_revision: Union[str, None] = 'b90b0154f05c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('external_id', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('players', 'external_id')
    # ### end Alembic commands ###