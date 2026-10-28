======================================
Linking solo queue accounts to players
======================================

In this example, we link a pro player, by name, to a solo queue account.

.. code-block:: python

   import os
   from sqlalchemy import select

   from ATG.database import get_session_factory
   from ATG.api import riot_client, get_account_by_riot_id
   from ATG.models import Player, Account

   client = riot_client(os.environ["RIOT_API"])
   Session = get_session_factory(os.environ["PROD_DB"])


   def link_pro(pro_name, soloq):
       with Session() as session:
           try:
               player = session.execute(
                   select(Player).where(Player.name == pro_name)
               ).scalar_one()
           except:
               print(f"Unable to find associated player for {pro_name}")
               return
           name, tagline = soloq.split("#")
           details = get_account_by_riot_id(client, name, tagline).json()
           new_acc = Account(
               puuid=details["puuid"],
               name=details["gameName"],
               tagline=details["tagLine"],
               region="NA1",
               player_id=player.id,
           )
           session.add(new_acc)
           try:
               session.commit()
               print(f"Linked {pro_name} with {name}#{tagline}")
           except:
               session.rollback()
               print(f"Account {name}#{tagline} already linked")


   link_pro("Tactical", "Tactical0#NA1")