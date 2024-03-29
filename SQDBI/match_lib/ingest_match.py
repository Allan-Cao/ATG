from datetime import timedelta
from SQDBI.api import get_match_history, get_match_by_id, get_match_string
from SQDBI.database import get_db
from SQDBI.models import Player, Game, Participant
from SQDBI.utils import SEASON_START
from .match_helper import parse_participant_dictionary
from tqdm import tqdm


def upsert_match_history(player: Player, api_key: str):
    db = next(get_db())
    for account in player.accounts:
        print(
            f"Updating match history for {account.account_name}#{account.account_tagline}"
        )
        # start_time = (
        #     SEASON_START.int_timestamp
        #     if account.latest_game is None
        #     else account.latest_game
        # )
        start_time = SEASON_START.int_timestamp
        # for now we are always starting from the beginning of the season
        
        match_ids = get_match_history(
            account.puuid,
            account.region,
            api_key,
            startTime=start_time,
        )

        final_time = 0

        for match_id in tqdm(match_ids):
            try:
                match = db.query(Game).filter(Game.id == match_id).first()
                if match is not None:
                    print(f"Game {match_id} already in the database. Skipping...")
                    continue

                game_data = get_match_by_id(match_id, account.region, api_key).json()
                game = Game(
                    id=match_id,
                    game_id=game_data["info"]["gameId"],
                    platform_id=game_data["info"]["platformId"],
                    game_creation=game_data["info"]["gameCreation"],
                    game_start=game_data["info"]["gameStartTimestamp"],
                    game_end=game_data["info"]["gameEndTimestamp"],
                    game_duration=game_data["info"]["gameDuration"],
                    game_type=game_data["info"]["gameType"],
                    game_version=game_data["info"]["gameVersion"],
                    queue_id=game_data["info"]["queueId"],
                )
                db.add(game)
                db.flush()

                for participant in game_data["info"]["participants"]:
                    participant_data = parse_participant_dictionary(participant)
                    p = Participant(
                        game_id=game.id,
                        game_duration=game.game_duration,
                        **participant_data,
                    )
                    db.add(p)

                db.commit()
                # print(f"Game {game.id} added to the database")
                if game_data["info"]["gameEndTimestamp"] > final_time:
                    final_time = game_data["info"]["gameEndTimestamp"]
            except Exception as e:
                print(f"Error processing match {match_id}: {e}")
                db.rollback()
            finally:
                db.close()
        if account.latest_game is None or final_time > account.latest_game:
            account.latest_game = final_time
            db.commit()
