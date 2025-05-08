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
BACKUP_Session = get_session_factory(os.environ["BACKUP_DB"])

batch_size = 100000

with BACKUP_Session() as backup_session:
    with Session() as session:
        for min_id in tqdm(range(0, 8904023, batch_size)):
            test = backup_session.execute(text(f"select id, win FROM participants WHERE id BETWEEN {min_id} AND {min_id + batch_size}")).all()
            bulk = [{"id": _[0], "win": _[1]} for _ in test]
            session.execute(update(Participant), bulk)
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error during migration: {str(e)}")
                break