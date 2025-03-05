from datetime import datetime, timedelta
from sqlalchemy import and_, select
from sqlalchemy.orm import Session as _Session
from tqdm import tqdm
from ..api import get_match_history, get_match_by_id
from ..api.account_v1 import get_account_by_puuid
from ..models import Player, Game, Participant, Account, TeamDto
from ..utils import SEASON_START, camel_to_snake, snake_to_camel


def update_account_names(session: _Session, API_KEY: str, days: int = 7):
    """Updates player account names/taglines"""
    update_delta = datetime.now() - timedelta(days=days)
    accounts_to_update = list(
        session.scalars(
            select(Account).where(
                and_(
                    Account.updated < update_delta,
                    Account.solo_queue_account == True,
                    Account.skip_update == False,
                )
            )
        )
    )
    if len(accounts_to_update) == 0:
        print("All accounts are up to date!")
        return
    for account in tqdm(accounts_to_update):
        account_details = get_account_by_puuid(account.puuid, API_KEY)
        account_details = account_details.json()
        account.name = account_details["gameName"]
        account.tagline = account_details["tagLine"]
    try:
        session.commit()
    except Exception as e:
        print(f"Something went wrong updating accounts: {str(e)}")
        session.rollback()


def upsert_match_history(
    session: _Session,
    player: Player,
    API_KEY: str,
    start_time: int = SEASON_START,
    start_latest: bool = True,
    queue_id: int = 420,
):
    existing_ids = set(session.scalars(select(Game.id)).all())
    for account in player.accounts or []:
        if not account.solo_queue_account or account.skip_update:
            continue
        print(f"Updating match history for {str(account)}")

        # To save on API calls, we should insert from season 14 start (for new accounts) or from the last known game.
        # However, startTime requires UNIX timestamps in Seconds while we are storing them in Miliseconds
        if account.latest_game is not None and start_latest:
            start_time = int(account.latest_game / 1000)
        match_ids = get_match_history(
            account.puuid,
            account.region,
            API_KEY,
            startTime=start_time,
            queue=queue_id,
        )
        new_match_ids = set(match_ids) - existing_ids

        if len(new_match_ids) == 0:
            print("All up to date!")
            continue

        latest_game_set = False
        for match_id in tqdm(new_match_ids):
            try:
                game_data = get_match_by_id(match_id, API_KEY)
                if game_data is None:
                    return None
                game_data = game_data.json()
                game_info = game_data["info"]
                match_end_time = upsert_match(session, match_id, game_data, game_info)
                if not latest_game_set and match_end_time is not None:
                    account.latest_game = match_end_time
                    latest_game_set = True
                existing_ids.add(match_id)
            except Exception as e:
                print(f"Failed to upsert match {match_id}: {str(e)}")
        session.commit()


def upsert_match(
    session: _Session,
    match_id: str,
    game_data: dict,
    game_info: dict,
    force: bool = False,
    game_type: str | None = None,
    tournament_info: dict = {},
) -> int | None:
    match = session.query(Game).filter(Game.id == match_id).first()
    # IF we are not forcing an update, we need to check the game doesn't already exist.
    if match is not None and force == False:
        return None
    # However, if we *are* forcing an update we will delete the existing records
    if force:
        session.query(Participant).filter(Participant.game_id == match_id).delete()
        session.query(TeamDto).filter(TeamDto.game_id == match_id).delete()
        session.query(Game).filter(Game.id == match_id).delete()
        session.commit()

    game = Game(
        **{k: game_info.get(snake_to_camel(k)) for k in Game.INFO_DTO},
        **{"id": match_id},
        **tournament_info,
    )
    session.add(game)
    session.flush()

    for team in game_info["teams"]:
        teamDto = TeamDto(
            game_id=game.id,
            bans=team["bans"],
            objectives=team["objectives"],
            team_id=team["teamId"],
            win=team["win"],
        )
        session.add(teamDto)

    # For some reason, zero duration game's are permitted by GRID. We can not process the match data for these games
    if game.game_duration and game.game_duration > 0:
        participants = []
        game_participants = game_info["participants"]
        for participant in game_participants:
            # First we extract the columns defined in the model and the DTOs we're storing
            participant_dto_columns = {
                camel_to_snake(k): v
                for k, v in participant.items()
                if camel_to_snake(k) in Participant.PARTICIPANT_DTO
            }
            stored_dtos = {
                camel_to_snake(k): participant[snake_to_camel(k)]
                for k in Participant.STORED_DTOS
            }
            # Then, we can remove the already stored keys DTOs
            for key in Participant.STORED_DTOS + Participant.PARTICIPANT_DTO:
                del participant[snake_to_camel(key)]
            # And store
            participant_dto = {camel_to_snake(k): v for k, v in participant.items()}
            participant_base = {
                "game_id": game.id,
                "game_duration": game.game_duration,
                "participant": participant_dto,
            }
            participants.append(
                Participant(
                    **participant_base, **participant_dto_columns, **stored_dtos
                )
            )
        session.add_all(participants)
        session.flush()
    try:
        session.commit()
        return game.game_end_timestamp
    except Exception as e:
        print(f"Something went wrong ingesting match {match_id}: {str(e)}")
        session.rollback()
