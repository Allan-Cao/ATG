"""Add general indexes to tables

Revision ID: 0933cdf8c8f7
Revises: 5a32fae4dd37
Create Date: 2025-07-04 13:21:20.283541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0933cdf8c8f7'
down_revision: Union[str, None] = '5a32fae4dd37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_draft_events_champion_id', 'draft_events', ['champion_id'], unique=False)
    op.create_index('idx_draft_events_game_id', 'draft_events', ['game_id'], unique=False)
    op.create_index('idx_draft_events_is_pick_turn', 'draft_events', ['is_pick', 'pick_turn'], unique=False)
    op.create_index('idx_games_game_type', 'games', ['game_type'], unique=False)
    op.create_index('idx_games_game_version', 'games', ['game_version'], unique=False)
    op.create_index('idx_games_series_id', 'games', ['series_id'], unique=False)
    op.create_index('idx_participants_champion_id', 'participants', ['champion_id'], unique=False)
    op.create_index('idx_series_tournament_id', 'series', ['tournament_id'], unique=False)
    op.create_index('idx_team_dtos_fk_team_id', 'team_dtos', ['fk_team_id'], unique=False)
    op.create_index('idx_team_dtos_game_id', 'team_dtos', ['game_id'], unique=False)
    op.create_index('idx_tournaments_league', 'tournaments', ['league'], unique=False)
    op.create_index('idx_tournaments_league_year', 'tournaments', ['league', 'year'], unique=False)
    op.create_index('idx_tournaments_year', 'tournaments', ['year'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_tournaments_year', table_name='tournaments')
    op.drop_index('idx_tournaments_league_year', table_name='tournaments')
    op.drop_index('idx_tournaments_league', table_name='tournaments')
    op.drop_index('idx_team_dtos_game_id', table_name='team_dtos')
    op.drop_index('idx_team_dtos_fk_team_id', table_name='team_dtos')
    op.drop_index('idx_series_tournament_id', table_name='series')
    op.drop_index('idx_participants_champion_id', table_name='participants')
    op.drop_index('idx_games_series_id', table_name='games')
    op.drop_index('idx_games_game_version', table_name='games')
    op.drop_index('idx_games_game_type', table_name='games')
    op.drop_index('idx_draft_events_is_pick_turn', table_name='draft_events')
    op.drop_index('idx_draft_events_game_id', table_name='draft_events')
    op.drop_index('idx_draft_events_champion_id', table_name='draft_events')
    # ### end Alembic commands ###
