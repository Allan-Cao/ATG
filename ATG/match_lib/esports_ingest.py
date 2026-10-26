from ..models import Player, Account, Participant
from sqlalchemy.orm import Session
from sqlalchemy import select


def create_player(name: str) -> Player:
    """Create a player object.

    :param name: Player name.
    :type name: str
    :returns: The created player object.
    :rtype: ATG.models.Player
    """
    return Player(name=name)


def create_account(
    puuid: str,
    name: str,
    tagline: str,
    player_id: int,
    region: str = "TOURNAMENT",
    skip_update: bool = True,
) -> Account:
    """Create an account object.

    :param puuid: Account identifier (PUUID / Account ID).
    :type puuid: str
    :param name: Account name.
    :type name: str
    :param tagline: Account tagline.
    :type tagline: str
    :param player_id: Player ID (foreign key).
    :type player_id: int
    :param region: Account region, defaults to ``"TOURNAMENT"``.
    :type region: str
    :param skip_update: Whether the account should be skipped when updating
        account names automatically, defaults to ``True``.
    :type skip_update: bool
    :returns: The created account object.
    :rtype: ATG.models.Account
    """
    return Account(
        puuid=puuid,
        name=name,
        tagline=tagline,
        region=region,
        player_id=player_id,
        skip_update=skip_update,
    )


def get_puuid(participant) -> str:
    return str(participant.get("puuid", participant["accountID"]))


def get_game_name(participant: dict) -> str:
    return (
        participant.get("riotId", {}).get("displayName")
        or participant.get("summonerName")
        or participant.get("playerName")
        or ""
    )


def get_tagline(participant) -> str:
    return participant.get("riotId", {}).get("tagLine", "")


def get_team_id(participant) -> int:
    return participant.get("teamID", participant.get("teamId"))


def parse_game_participants(
    participants: list[dict],
    game_id: str,
    winning_team_id: int,
    NAME_ID_MAP: dict[str, int],
) -> list[Participant]:
    """Parse the participants into a list of :class:`~ATG.models.Participant` objects.

    :param participants: List of game participants.
    :type participants: list[dict]
    :param game_id: Riot's game ID number (foreign key).
    :type game_id: str
    :param winning_team_id: ``100`` or ``200`` (blue/red winners).
    :type winning_team_id: int
    :param NAME_ID_MAP: Champion name to champion ID map.
    :type NAME_ID_MAP: dict[str, int]
    :returns: The parsed participant objects.
    :rtype: list[ATG.models.Participant]
    """
    game_participants = []
    for participant in participants:
        game_participants.append(
            Participant(
                game_id=game_id,
                puuid=get_puuid(participant),
                participant_id=participant["participantID"],
                riot_id_game_name=get_game_name(participant),
                riot_id_tagline=get_tagline(participant),
                summoner_id=participant["accountID"],
                team_id=get_team_id(participant),
                champion_id=NAME_ID_MAP[participant["championName"].lower()],
                win=get_team_id(participant) == winning_team_id,
            )
        )
    return game_participants


def get_common_prefix_length(player_names: list[str]) -> int:
    """Get the number of characters shared in the prefix of all items of a list.

    :param player_names: A list of player names.
    :type player_names: list[str]
    :returns: The length of the shared prefix.
    :rtype: int
    """
    common_prefix_length = 0
    for chars in zip(*player_names):
        if len(set(chars)) == 1:
            common_prefix_length += 1
        else:
            break
    return common_prefix_length


def create_missing_accounts(session: Session, participants: dict):
    """Parse a list of participants, adding any missing players/accounts to the session.

    :param session: Active SQLAlchemy session object.
    :type session: sqlalchemy.orm.Session
    :param participants: A MatchV5-like participant list.
    :type participants: list[dict]
    """
    stored_puuids = session.scalars(select(Account.puuid)).all()
    for participant in participants:
        puuid = get_puuid(participant)
        if puuid not in stored_puuids:
            game_name = get_game_name(participant)
            player_names = [
                get_game_name(p)
                for p in participants
                if get_team_id(p) == get_team_id(participant)
            ]
            player_name = game_name[get_common_prefix_length(player_names) :]

            db_player = session.scalar(select(Player).where(Player.name == player_name))

            if db_player is None:
                db_player = create_player(player_name)
                session.add(db_player)
                session.flush()

            session.add(
                create_account(puuid, game_name, get_tagline(participant), db_player.id)
            )
