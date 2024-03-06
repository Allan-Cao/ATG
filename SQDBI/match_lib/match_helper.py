__version__ = 'dev'
from cassiopeia import Match, Items
from cassiopeia.core.match import Participant
from datetime import timedelta

# Constants
MINIMUM_MATCH_DURATION = timedelta(minutes=10)
SCHEMA = [
    "item_0",
    "item_1",
    "item_2",
    "item_3",
    "item_4",
    "item_5",
    "trinket",
    "patch",
    "match",
    "created",
    "duration",
    "account",
    "champion",
    "lane",
    "win",
    "kda",
    "kills",
    "deaths",
    "assists",
    "total_cs",
    "cspm",
    "level",
    "primary",
    "secondary",
    "summoner_d",
    "summoner_f",
    "puuid",
]


def get_english_name(cass_obj) -> str:
    """
    Returns the English name of an item.

    Args:
        cass_obj (cassiopeia.core.staticdata.staticdataobject.StaticDataObject): A Cassiopeia object.
    
    Returns:
        str: The English name of the object.
    """
    return type(cass_obj)(id=cass_obj.id, region="NA", version=cass_obj.version).name

def get_item_names(items: Items) -> list:
    """
    Returns a list of item names, replacing None with "-".

    Args:
        items (list): A list of items.

    Returns:
        list: A list of item names.
    """
    return [get_english_name(item) if item else "-" for item in items]


def region_string(match: Match) -> str:
    """
    Returns a formatted string containing the platform and match ID.

    Args:
        match (Match): A Match object.

    Returns:
        str: A formatted string with platform and match ID.
    """
    return f"{match.platform.value}_{match.id}"

def account_name(account: list) -> str:
    return f"{account['account_name']}#{account['tagline']}"

def get_player_stats(player, account, match) -> list:
    """
    Returns a list of player stats for a given match.

    Args:
        player (Participant): A Participant object.
        match (Match): A Match object.

    Returns:
        list: A list of player stats.
    """
    player_build = get_item_names(player.stats.items)
    try:
        team_position = player.team_position.name if player.team_position else ""
    except:
        team_position = ""
    return player_build + [
        match.patch.majorminor,
        region_string(match),
        match.creation.to("US/Pacific").format("YYYY-MM-DD HH:mm:ss"),
        match.duration.total_seconds(),
        account_name(account),
        get_english_name(player.champion),
        team_position,
        player.stats.win,
        player.stats.kda,
        player.stats.kills,
        player.stats.deaths,
        player.stats.assists,
        (player.stats.neutral_minions_killed + player.stats.total_minions_killed),
        (player.stats.neutral_minions_killed + player.stats.total_minions_killed)
        / match.duration.total_seconds()
        * 60,
        player.stats.level,
        get_english_name(player.runes.keystone),
        list(player.runes)[-1].path.name,  # Need to somehow deal with the non-english possibilty later #TODO haha
        get_english_name(player.summoner_spell_d),
        get_english_name(player.summoner_spell_f),
        player.summoner.puuid,
    ]