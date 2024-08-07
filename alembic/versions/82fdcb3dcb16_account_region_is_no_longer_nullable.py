"""Account region is no longer nullable

Revision ID: 82fdcb3dcb16
Revises: 5b4297d7f974
Create Date: 2024-08-07 08:49:39.579287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82fdcb3dcb16'
down_revision: Union[str, None] = '5b4297d7f974'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'region',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accounts', 'region',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###