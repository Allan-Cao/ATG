from typing import Optional
from ..utils import Side
from ..models import Game

def extract_major_minor_patch(game_version: str) -> str:
    version_parts = game_version.split(".")
    if len(version_parts) >= 2:
        return f"{version_parts[0]}.{version_parts[1]}"
    else:
        raise ValueError(f"Expecting major/minor patch format received: {game_version}")


def parse_participant_dictionary(player: dict) -> dict:
    # We parse the raw riot data to produce a format that can be used to create a Participant object
    return {
        "puuid": player["puuid"],
        "account_name": player.get("riotIdGameName"),
        "account_tagline": player.get("riotIdTagline"),
        "side": Side(player["teamId"]).name,
        "win": player["win"],
        "team_position": player["teamPosition"],
        "lane": player["lane"],
        "champion": player["championName"],
        "champion_id": player["championId"],
        "kills": player["kills"],
        "deaths": player["deaths"],
        "assists": player["assists"],
        "summoner1_id": player.get("summoner1Id"),  # Missing from GRID
        "summoner2_id": player.get("summoner2Id"),
        "gold_earned": player["goldEarned"],
        "total_minions_killed": player["totalMinionsKilled"],
        "total_neutral_minions_killed": player["totalAllyJungleMinionsKilled"]
        + player["totalEnemyJungleMinionsKilled"],
        "total_ally_jungle_minions_killed": player["totalAllyJungleMinionsKilled"],
        "total_enemy_jungle_minions_killed": player["totalEnemyJungleMinionsKilled"],
        "early_surrender": player["gameEndedInEarlySurrender"],
        "surrender": player["gameEndedInSurrender"],
        "first_blood": player["firstBloodKill"],
        "first_blood_assist": player["firstBloodAssist"],
        "first_tower": player["firstTowerKill"],
        "first_tower_assist": player["firstTowerAssist"],
        "damage_dealt_to_buildings": player["damageDealtToBuildings"],
        "turret_kills": player["turretKills"],
        "turrets_lost": player["turretsLost"],
        "damage_dealt_to_objectives": player["damageDealtToObjectives"],
        "dragon_kills": player["dragonKills"],
        "objectives_stolen": player["objectivesStolen"],
        "longest_time_spent_living": player["longestTimeSpentLiving"],
        "largest_killing_spree": player["largestKillingSpree"],
        "total_damage_dealt_champions": player["totalDamageDealtToChampions"],
        "total_damage_taken": player["totalDamageTaken"],
        "total_damage_self_mitigated": player["damageSelfMitigated"],
        "total_damage_shielded_teammates": player["totalDamageShieldedOnTeammates"],
        "total_heals_teammates": player["totalHealsOnTeammates"],
        "total_time_crowd_controlled": player["totalTimeCCDealt"],
        "total_time_spent_dead": player["totalTimeSpentDead"],
        "vision_score": player["visionScore"],
        "wards_killed": player["wardsKilled"],
        "wards_placed": player["wardsPlaced"],
        "control_wards_placed": player["detectorWardsPlaced"],
        "item0": player["item0"],
        "item1": player["item1"],
        "item2": player["item2"],
        "item3": player["item3"],
        "item4": player["item4"],
        "item5": player["item5"],
        "item6": player["item6"],
        "perk_keystone": player["perks"]["styles"][0]["selections"][0]["perk"],
        "perk_primary_row_1": player["perks"]["styles"][0]["selections"][1]["perk"],
        "perk_primary_row_2": player["perks"]["styles"][0]["selections"][2]["perk"],
        "perk_primary_row_3": player["perks"]["styles"][0]["selections"][3]["perk"],
        "perk_secondary_row_1": player["perks"]["styles"][1]["selections"][0]["perk"],
        "perk_secondary_row_2": player["perks"]["styles"][1]["selections"][1]["perk"],
        "perk_primary_style": player["perks"]["styles"][0]["style"],
        "perk_secondary_style": player["perks"]["styles"][1]["style"],
        "perk_shard_defense": player["perks"]["statPerks"]["defense"],
        "perk_shard_flex": player["perks"]["statPerks"]["flex"],
        "perk_shard_offense": player["perks"]["statPerks"]["offense"],
    }


def process_match_metadata(
    game_data, match_id, game_type: Optional[str] = None
) -> Game:
    if game_data.get("endOfGameResult") == "Abort_Unexpected":
        game = Game(
            id=match_id,
            game_id=match_id.split("_")[1],
            platform_id=match_id.split("_")[0],
            game_creation=game_data["gameCreation"],
            game_start=game_data["gameStartTimestamp"],
            game_end=game_data["gameEndTimestamp"],
            game_duration=game_data["gameDuration"],
            game_type=game_type or game_data["gameType"],
            patch=extract_major_minor_patch(game_data["gameVersion"]),
            queue_id=game_data["queueId"],
        )
    else:
        game = Game(
            id=match_id,
            game_id=game_data["gameId"],
            platform_id=game_data["platformId"],
            game_creation=game_data["gameCreation"],
            game_start=game_data["gameStartTimestamp"],
            game_end=game_data["gameEndTimestamp"],
            game_duration=game_data["gameDuration"],
            game_type=game_type or game_data["gameType"],
            patch=extract_major_minor_patch(game_data["gameVersion"]),
            queue_id=game_data["queueId"],
        )
    return game
