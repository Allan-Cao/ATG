"""Increase team code length

Revision ID: 771e3aba1a6f
Revises: ac518c8b7d22
Create Date: 2024-10-04 00:03:36.915670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '771e3aba1a6f'
down_revision: Union[str, None] = 'ac518c8b7d22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('teams', 'team_code',
               existing_type=sa.VARCHAR(length=5),
               type_=sa.String(length=10),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('teams', 'team_code',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=5),
               existing_nullable=True)
    # ### end Alembic commands ###
