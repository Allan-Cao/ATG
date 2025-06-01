"""Change team/tournament primary key datatypes to text

Revision ID: fc71cacb307e
Revises: e3afb86e041e
Create Date: 2025-05-31 22:56:50.319372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc71cacb307e'
down_revision: Union[str, None] = 'e3afb86e041e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("series_tournament_id_fkey", "series")
    op.drop_constraint("team_dtos_fk_team_id_fkey", "team_dtos")
    op.drop_constraint("player_team_associations_team_id_fkey", "player_team_associations")

    op.alter_column('teams', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('tournaments', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=False)
    
    op.alter_column('series', 'tournament_id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('team_dtos', 'fk_team_id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('player_team_associations', 'team_id',
               existing_type=sa.INTEGER(),
               type_=sa.Text(),
               existing_nullable=False)
    
    
    op.create_foreign_key(
        'series_tournament_id_fkey', 
        'series', 'tournaments',
        ['tournament_id'], ['id']
    )
    op.create_foreign_key(
        'team_dtos_fk_team_id_fkey', 
        'team_dtos', 'teams',
        ['fk_team_id'], ['id']
    )
    op.create_foreign_key(
        'player_team_associations_team_id_fkey', 
        'player_team_associations', 'teams',
        ['team_id'], ['id']
    )


def downgrade() -> None:
    op.drop_constraint("series_tournament_id_fkey", "series")
    op.drop_constraint("team_dtos_fk_team_id_fkey", "team_dtos")
    op.drop_constraint("player_team_associations_team_id_fkey", "player_team_associations")

    op.alter_column('series', 'tournament_id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('team_dtos', 'fk_team_id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('player_team_associations', 'team_id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    
    op.alter_column('teams', 'id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('tournaments', 'id',
               existing_type=sa.Text(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    
    op.create_foreign_key(
        'series_tournament_id_fkey',
        'series', 'tournaments',
        ['tournament_id'], ['id']
    )
    op.create_foreign_key(
        'team_dtos_fk_team_id_fkey',
        'team_dtos', 'teams',
        ['fk_team_id'], ['id']
    )
    op.create_foreign_key(
        'player_team_associations_team_id_fkey',
        'player_team_associations', 'teams',
        ['team_id'], ['id']
    )
