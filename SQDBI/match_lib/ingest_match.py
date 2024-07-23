import datetime
from sqlalchemy.orm import Session as _Session
from tqdm import tqdm
from SQDBI.api import get_match_history, get_match_by_id, get_match_string
from SQDBI.api.account_v1 import get_account_by_puuid
from SQDBI.database import Session
from SQDBI.models import Player, Game, Participant, Account
from SQDBI.utils import SEASON_START
from .match_helper import parse_participant_dictionary, extract_major_minor_version


def upsert_match_history(session: _Session, player: Player, API_KEY: str):
    for account in player.accounts or []:
        if account.last_update < (datetime.datetime.now() - datetime.timedelta(days=7)):
            try:
                account = update_account_riotid(session, account, API_KEY)
            except Exception as e:
                print(f"Something went wrong updating account details: {str(e)}")
                session.rollback()
        print(
            f"Updating match history for {account.account_name}#{account.account_tagline}"
        )
        start_time = (
            SEASON_START.int_timestamp
            if account.latest_game is None
            else account.latest_game
        )

        match_ids = get_match_history(
            account.puuid,
            account.region,
            API_KEY,
            startTime=start_time,
        )

        final_time = 0

        for match_id in tqdm(match_ids):
            try:
                match_end_time = upsert_match(
                    session, match_id, account.region, API_KEY
                )
                if match_end_time is not None and match_end_time > final_time:
                    final_time = match_end_time
            except:
                print(f"Failed to process match {match_id}")
        if account.latest_game is None or final_time > account.latest_game:
            account.latest_game = final_time
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


def process_match_metadata(game_data, match_id) -> Game:
    version_major, version_minor = extract_major_minor_version(
        game_data["info"]["gameVersion"]
    )
    game = Game(
        id=match_id,
        game_id=game_data["info"]["gameId"],
        platform_id=game_data["info"]["platformId"],
        game_creation=game_data["info"]["gameCreation"],
        game_start=game_data["info"]["gameStartTimestamp"],
        game_end=game_data["info"]["gameEndTimestamp"],
        game_duration=game_data["info"]["gameDuration"],
        game_type=game_data["info"]["gameType"],
        game_version_major=version_major,
        game_version_minor=version_minor,
        queue_id=game_data["info"]["queueId"],
    )
    return game


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


def update_account_riotid(session: _Session, account: Account, API_KEY: str):
    account = session.merge(account)
    account_details = get_account_by_puuid(account.puuid, API_KEY)
    if account_details is None:
        raise ValueError(f"No account details found for PUUID: {account.puuid}")
    # Update the account object
    account.account_name = account_details.get("gameName")
    account.account_tagline = account_details.get("tagLine")
    return account
