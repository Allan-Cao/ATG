headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en-CA;q=0.9,en;q=0.8,ru-RU;q=0.7,ru;q=0.6,ko-KR;q=0.5,ko;q=0.4",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

# The AMERICAS routing value serves NA, BR, LAN and LAS. The ASIA routing value serves KR and JP. The EUROPE routing value serves EUNE, EUW, ME1, TR and RU. The SEA routing value serves OCE, SG2, TW2 and VN2.
platform_routing = {
    "NA1": "americas",
    "BR1": "americas",
    "LA1": "americas",
    "LA2": "americas",
    "KR": "asia",
    "JP": "asia",
    "ME1": "europe",
    "EUN1": "europe",
    "EUW1": "europe",
    "TR1": "europe",
    "RU": "europe",
    "OC1": "sea",
    "SG2": "sea",
    "TW2": "sea",
    "VN2": "sea",
}

REGIONS = platform_routing.keys()


def parse_match_id(match_id: str) -> tuple[str, str]:
    split = match_id.split("_")
    if len(split) != 2 or split[0] not in platform_routing.keys():
        raise ValueError("Invalid match_id received")
    return split[0], split[1]
