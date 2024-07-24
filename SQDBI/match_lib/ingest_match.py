import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session as _Session
from typing import List, Set
from tqdm import tqdm
from SQDBI.api import get_match_history, get_match_by_id, get_match_string
from SQDBI.api.account_v1 import get_account_by_puuid
from SQDBI.database import Session
from SQDBI.models import Player, Game, Participant, Account
from SQDBI.utils import SEASON_START
from .match_helper import (
    parse_participant_dictionary,
    extract_major_minor_version,
    process_match_metadata,
)


def update_player_accounts(session: _Session, API_KEY: str):
    accounts_to_update = session.scalars(
        select(Account).where(
            Account.last_update < (datetime.datetime.now() - datetime.timedelta(days=7))
        )
    )
    if len(accounts_to_update.all()) == 0:
        print("All accounts are up to date!")
        return
    for account in tqdm(accounts_to_update.all()):
        account_details = get_account_by_puuid(account.puuid, API_KEY)
        if account_details is None:
            print(f"No account details found for PUUID: {account.puuid}")
            continue
        account.account_name = account_details.get("gameName")
        account.account_tagline = account_details.get("tagLine")
        account.last_update = datetime.datetime.now()
    try:
        session.commit()
    except Exception as e:
        print(f"Something went wrong updating accounts: {str(e)}")
        session.rollback()


def upsert_match_history(
    session: _Session,
    existing_ids: Set,
    player: Player,
    API_KEY: str,
    start_time: int = SEASON_START,
):
    for account in player.accounts or []:
        print(
            f"Updating match history for {account.account_name}#{account.account_tagline}"
        )

        match_ids = get_match_history(
            account.puuid,
            account.region,
            API_KEY,
            startTime=start_time,
            queue=420,
        )

        new_match_ids = set(match_ids) - existing_ids
        if len(new_match_ids) == 0:
            print("All up to date!")
            continue

        latest_game_set = False
        for match_id in tqdm(new_match_ids):
            try:
                match_end_time = upsert_match(
                    session, match_id, account.region, API_KEY
                )
                if not latest_game_set:
                    account.latest_game = match_end_time
                    latest_game_set = True
                existing_ids.add(match_id)
            except:
                print(f"Failed to process match {match_id}")
        session.commit()


def upsert_match(
    session: _Session, match_id: str, region: str, api_key: str, force: bool = False
):
    match = session.query(Game).filter(Game.id == match_id).first()
    # IF we are not forcing an update, we need to check the game doesn't already exist.
    if match is not None and force == False:
        return None
    # However, if we *are* forcing an update we will delete the existing records
    if force:
        session.query(Participant).filter(Participant.game_id == match_id).delete()
        session.query(Game).filter(Game.id == match_id).delete()
        session.commit()

    game_data = get_match_by_id(match_id, region, api_key).json()
    game = process_match_metadata(game_data, match_id)
    session.add(game)
    session.flush()

    participants = process_match_participants(game, game_data)
    session.add_all(participants)
    session.flush()
    return game_data["info"]["gameEndTimestamp"]


def process_match_participants(game, game_data) -> list[Participant]:
    participants = []
    for participant in game_data["info"]["participants"]:
        participant_data = parse_participant_dictionary(participant)
        p = Participant(
            game_id=game.id,
            game_duration=game.game_duration,
            **participant_data,
        )
        participants.append(p)
    return participants
