# I'm assuming nobody is using this library BUT if you were to be on the old version,
# You would first run this script with the new participant_stat.py file (added to __init__.py)
# Then run the alembic migration that removes the stats from participant.py

import sys

sys.path.append("..")

import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import *

from ATG.database import get_session_factory
from ATG.match_lib import *
from ATG.models import *
from ATG.api import *

from tqdm import tqdm

Session = get_session_factory(os.environ["PROD_DB"])

batch_size = 25000
offset = 0
with Session() as session:
    total_participants = session.scalar(
        select(func.count()).select_from(Participant).filter(
                ~exists().where(
                    ParticipantStat.participant_id == Participant.id
                )
            ))
    print(f"Found {total_participants} participants to migrate")

    while True:
        old_participants = session.scalars(
            select(Participant)
            .filter(
                ~exists().where(
                    ParticipantStat.participant_id == Participant.id
                )
            )
            .offset(offset).order_by(Participant.id).limit(batch_size)).all()
        if len(old_participants) == 0:
            break
        new_stats = []
        for old_part in tqdm(old_participants):
            if old_part.kills is None:
                # We're likely dealing with esports data which will require reprocessing at a later date.
                empty = {_: 0 for _ in ParticipantStat.PARTICIPANT_STAT_DTO}
                new_stat = ParticipantStat(
                    participant_id = old_part.id,
                    **empty,
                    source_data = {},
                )
            else:
                new_source_data = old_part.participant
                new_source_data["challenges"] = old_part.challenges
                new_source_data["missions"] = old_part.missions
                new_source_data["perks"] = old_part.perks
                
                new_stat = ParticipantStat(
                    participant_id = old_part.id,
                    kills = old_part.kills,
                    deaths = old_part.deaths,
                    assists = old_part.assists,
                    total_minions_killed = old_part.total_minions_killed,
                    neutral_minions_killed = old_part.neutral_minions_killed,
                    item_0 = old_part.participant['item0'],
                    item_1 = old_part.participant['item1'],
                    item_2 = old_part.participant['item2'],
                    item_3 = old_part.participant['item3'],
                    item_4 = old_part.participant['item4'],
                    item_5 = old_part.participant['item5'],
                    item_6 = old_part.participant['item6'],
                    summoner_1_id = old_part.participant.get('summoner1_id', 0),
                    summoner_2_id = old_part.participant.get('summoner2_id', 0),
                    source_data = new_source_data,
                )
            new_stats.append(new_stat)
        session.add_all(new_stats)
        offset += batch_size
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error during migration: {str(e)}")
            import traceback
            traceback.print_exc()
            break