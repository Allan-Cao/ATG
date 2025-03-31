"""add participant_id

Revision ID: 04092ec444b2
Revises: ba40f60cb515
Create Date: 2025-03-29 21:16:24.022525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04092ec444b2'
down_revision: Union[str, None] = 'ba40f60cb515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participants', sa.Column('participant_id', sa.Integer(), nullable=False, server_default="-1"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participants', 'participant_id')
    # ### end Alembic commands ###
