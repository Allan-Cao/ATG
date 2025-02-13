import os
from dotenv import load_dotenv

load_dotenv()

from ATG.match_lib import upsert_match_history, update_account_names
from ATG.database import get_session_factory
from ATG.models import Player, Account
from sqlalchemy import exists

RIOT_API = os.environ["RIOT_API"]
DB_CONNECTION = os.environ["DB_CONNECTION"]

Session = get_session_factory(DB_CONNECTION)

with Session() as session:
    update_account_names(session, RIOT_API)
    PLAYERS = (
        session.query(Player)
        .filter(
            exists().where(
                (Account.player_id == Player.id) & Account.solo_queue_account
            )
        )
        .all()
    )
    for player in PLAYERS:
        upsert_match_history(session, player, RIOT_API)
