"""Adds account flags

Revision ID: 01a2faf46c42
Revises: 82fdcb3dcb16
Create Date: 2024-10-03 20:37:55.017674

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import false
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "01a2faf46c42"
down_revision: Union[str, None] = "82fdcb3dcb16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accounts",
        sa.Column("skip_update", sa.Boolean(), nullable=False, server_default=false()),
    )
    op.add_column(
        "accounts",
        sa.Column(
            "account_details", sa.SmallInteger(), nullable=False, server_default="0"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("accounts", "account_details")
    op.drop_column("accounts", "skip_update")
    # ### end Alembic commands ###
