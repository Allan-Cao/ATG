from dotenv import load_dotenv

load_dotenv(override=True)

from ATG.database import get_session_factory
from ATG.models import ParticipantStat
import os
from sqlalchemy import select, func
from sqlalchemy.orm import attributes

Session = get_session_factory(os.environ["PROD_DB"])


batch_size = 5000
offset = 0

with Session() as session:
    total_participants = session.scalar(
        select(func.count()).select_from(ParticipantStat)
    )
    print(f"Found {total_participants} participants to migrate")

    while True:
        old_stats = session.scalars(
            select(ParticipantStat)
            .filter(ParticipantStat.champ_level.is_(None))
            .offset(offset)
            .order_by(ParticipantStat.id)
            .limit(batch_size)
        ).all()

        if not old_stats:
            break

        for old in old_stats:
            try:
                data = dict(old.source_data or {})

                for column in ParticipantStat.PARTICIPANT_STAT_DTO:
                    val = data.pop(column, None)
                    if val is not None:
                        setattr(old, column, val)

                old.perks = data.get("perks")
                old.total_time_CC_dealt = int(data.get("total_time_c_c_dealt", 0))
                old.time_CC_ing_others = int(data.get("time_c_cing_others", 0))
                old.total_gold = int(data.get("gold_earned", 0))
                old.current_gold = int(
                    data.get("gold_earned", 0) - data.get("gold_spent", 0)
                )

                for key in [
                    "perks",
                    "total_time_c_c_dealt",
                    "time_c_cing_others",
                    "gold_earned",
                    "gold_spent",
                ]:
                    data.pop(key, None)

                old.source_data = data
                attributes.flag_modified(old, "source_data")
                session.add(old)
            except Exception as e:
                print(f"Error processing record ID {old.id}: {str(e)}")
                continue

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error committing batch at offset {offset}: {str(e)}")
            import traceback

            traceback.print_exc()
            break

        offset += batch_size
