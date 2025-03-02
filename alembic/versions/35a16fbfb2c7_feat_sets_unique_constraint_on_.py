"""feat: Sets unique constraint on champions table entries

Revision ID: 35a16fbfb2c7
Revises: 7c63f7c2aa33
Create Date: 2025-02-28 22:17:04.758177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35a16fbfb2c7'
down_revision: Union[str, None] = '7c63f7c2aa33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'champions', ['alias'])
    op.create_unique_constraint(None, 'champions', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'champions', type_='unique')
    op.drop_constraint(None, 'champions', type_='unique')
    # ### end Alembic commands ###
