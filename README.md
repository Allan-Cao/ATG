# ATG - All The Games

Opinionated but flexible library of database models and scripts to store solo queue / competitive player and game data tailored for LoL Esports.

#### Verson 1.0
As of version 1.0, PostgreSQL is the required database backend since JSONB columns are extensively used to easily store game stats while minimizing schema changes.

Although I've decided to use a version number >= 1, do expect schema changes and functionality to break at any point. With the use of JSONB columns, the core schema and functionality of the library, storing Match-V5 JSONs/Riot "summary" files and accounts linked to players will remain stable. However, expect changes to the esports tournament/draft models as I look to add support for saving drafts / additional match information.


## Features
- Functions to access Riot & GRID APIs with smart region handling
- SQLAlchemy database models compatible with both solo queue & esports games
- Database models to store riot game event JSONL files
- Ability to store complete Match-V5 JSON objects
- Scripts to insert/manage solo queue accounts & store new solo queue games

## Todo
- [x] Remove the usage of `ratelimit` in favor of something that actually does stable rate limiting
- [x] Properly handle API error codes
- [ ] Handle database sessions and API keys better using dependency injection or something other than passing session objects around.
- [x] Add the ability to store draft / other available esports game information
- [x] Open source GRID API code and GRID insertion scripts

## Setup & Example Usage

It is recommended to use a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) when directly running this library's scripts.

Setup dependencies
```bash
pip install -r requirements.txt
```

Edit the .env file with your Riot API key and database connection string. The [psycopg3 database driver](https://www.psycopg.org/psycopg3/docs/basic/install.html) is installed and recommended.

```bash
python main.py
```

Example usage (linking a pro player by name to a solo queue account)
```python
import os
from sqlalchemy import select

from ATG.database import get_session_factory
from ATG.api import get_account_by_riot_id
from ATG.models import Player, Account

RIOT_API = os.environ["RIOT_API"]
Session = get_session_factory(os.environ["PROD_DB"])

def link_pro(pro_name, soloq):
    with Session() as session:
        try:
            player = session.execute(select(Player).where(Player.name == pro_name)).scalar_one()
        except:
            print(f"Unable to find associated player for {pro_name}")
            return
        name, tagline = soloq.split("#")
        details = get_account_by_riot_id(name, tagline, RIOT_API).json()
        new_acc = Account(puuid=details['puuid'], name=details['gameName'], tagline=details['tagLine'], region='NA1', player_id=player.id)
        session.add(new_acc)
        try:
            session.commit()
            print(f"Linked {pro_name} with {name}#{tagline}")
        except:
            session.rollback()
            print(f"Account {name}#{tagline} already linked")

link_pro("Tactical", "Tactical0#NA1")
```

## Schema changes - Alembic commands

In the case of schema changes, Alembic allows us to automatically generate a script to apply the changes to the database. When a commit will cause a schema change, an alembic script should be attached to the commit.

```bash
alembic revision --autogenerate -m "changes"
alembic upgrade head
```

## Legal
ATG is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc
