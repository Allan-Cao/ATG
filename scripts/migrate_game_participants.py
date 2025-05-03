# Created with the assistance of Claude 3.5

import sys

sys.path.append("..")

import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import *
from tqdm import tqdm

from ATG.database import get_session_factory
from ATG.match_lib import *
from ATG.models import *
from ATG.api import *

RIOT_API = os.environ["RIOT_API"]
Session = get_session_factory(os.environ["DB_CONNECTION"])

role_map = {
    1: "TOP",
    2: "JUNGLE",
    3: "MIDDLE",
    4: "BOTTOM",
    5: "UTILITY",
    6: "TOP",
    7: "JUNGLE",
    8: "MIDDLE",
    9: "BOTTOM",
    10: "UTILITY",

}

with Session() as session:
    old_participants = session.scalars(select(GameParticipant)).all()
    print(f"Found {len(old_participants)} GameParticipant objects to migrate")

    champions = session.scalars(select(Champion)).all()
    champion_name_to_id = {champ.name: champ.id for champ in champions}
    champion_alias_to_name = {champ.alias: champ.name for champ in champions}

    games = session.scalars(select(Game)).all()
    game_id_to_duration = {game.id: game.game_duration for game in games if game.game_duration is not None}

    created_count = 0
    updated_count = 0
    skipped_count = 0

    for old_part in tqdm(old_participants):
        champion_name = champion_alias_to_name.get(old_part.champion)
        if not champion_name:
            print(f"Warning: Champion alias {old_part.champion} not found in Champions table")
            skipped_count += 1
            continue

        champion_id = champion_name_to_id.get(champion_name)
        if not champion_id:
            print(f"Warning: Champion name {champion_name} not found in Champions table")
            skipped_count += 1
            continue

        existing_participant = session.scalar(
            select(Participant).where(
                (Participant.game_id == old_part.game_id) &
                (Participant.puuid == old_part.puuid)
            )
        )

        game_duration = game_id_to_duration.get(old_part.game_id, 0)

        if existing_participant:
            existing_participant.champion_id = champion_id
            existing_participant.champion_name = champion_name
            existing_participant.team_id = old_part.side
            existing_participant.participant_id = old_part.participant_id

            if not existing_participant.riot_id_game_name:
                existing_participant.riot_id_game_name = old_part.display_name
            if not existing_participant.riot_id_tagline:
                existing_participant.riot_id_tagline = "eProd"
            if not existing_participant.summoner_id:
                existing_participant.summoner_id = old_part.account_id
            if not existing_participant.summoner_name:
                existing_participant.summoner_name = old_part.display_name
            if not existing_participant.win:
                existing_participant.win = old_part.win

            if existing_participant.game_duration == 0:
                existing_participant.game_duration = game_duration

                if existing_participant.total_cs is not None:
                    existing_participant.cspm = existing_participant.calculate_cspm()

            updated_count += 1
        else:
            new_part = Participant(
                game_id=old_part.game_id,
                puuid=old_part.puuid,
                champion_id=champion_id,
                champion_name=champion_name,
                team_id=old_part.side,
                participant_id=old_part.participant_id,

                riot_id_game_name=old_part.display_name,
                riot_id_tagline="eProd",
                summoner_id=old_part.account_id,
                summoner_name=old_part.display_name,

                # Game stats
                win=old_part.win,
                team_position=role_map[old_part.participant_id],

                # Set game_duration from the game if available
                game_duration=game_duration,

                # Initialize empty JSONs
                challenges={},
                missions={},
                perks={},
                participant={}
            )

            session.add(new_part)
            created_count += 1

    # Print summary before committing
    print(f"Created {created_count} new Participant objects")
    print(f"Updated {updated_count} existing Participant objects")
    print(f"Skipped {skipped_count} GameParticipant objects due to missing data")

    try:
        session.commit()
        print("Successfully migrated GameParticipant objects to Participant")
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {str(e)}")
        import traceback
        traceback.print_exc()
