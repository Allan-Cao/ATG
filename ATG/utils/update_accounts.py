from pygsheets import Worksheet
from ..api import get_account_by_puuid, get_account_by_riot_id
from collections import defaultdict
from datetime import datetime


def update_player_accounts(sh: Worksheet, api_key: str) -> list:
    account_df = sh.worksheet("title", "accounts").get_as_df()

    player_accounts = defaultdict(list)

    updated_details = [["puuid", "last_update"]]

    for idx, row in account_df.iterrows():
        if row["puuid"] == "":
            row["puuid"] = get_account_by_riot_id(
                row["account_name"], row["tagline"], api_key
            )["puuid"]
            row["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Recheck the account name and tagline if it's been over a week
        elif (
            datetime.now() - datetime.strptime(row["last_update"], "%Y-%m-%d %H:%M:%S")
        ).days > 7:
            account_details = get_account_by_puuid(row["puuid"], api_key)
            row["account_name"] = account_details["gameName"]
            row["tagline"] = account_details["tagLine"]
            row["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        player = row["player_name"]

        player_accounts[player].append(
            {
                "puuid": row["puuid"],
                "region": row["region"],
                "account_name": row["account_name"],
                "tagline": row["tagline"],
            }
        )
        updated_details.append([row["puuid"], row["last_update"]])

    sh.worksheet("title", "accounts").update_values("G:H", updated_details)

    return player_accounts
