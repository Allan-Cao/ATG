headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en-CA;q=0.9,en;q=0.8,ru-RU;q=0.7,ru;q=0.6,ko-KR;q=0.5,ko;q=0.4",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

## The americas routing value serves NA, BR, LAN and LAS. The asia routing value serves KR and JP. The europe routing value serves EUNE, EUW, TR and RU. The sea routing value serves OCE, PH2, SG2, TH2, TW2 and VN2.
routing = {
    "NA": "americas",
    "BR": "americas",
    "LAN": "americas",
    "LAS": "americas",
    "KR": "asia",
    "JP": "asia",
    "EUNE": "europe",
    "EUW": "europe",
    "TR": "europe",
    "RU": "europe",
    "OCE": "sea",
    "PH2": "sea",
    "SG2": "sea",
    "TH2": "sea",
    "TW2": "sea",
    "VN2": "sea",
}

server_string = {
    "NA": "NA1",
    "BR": "BR1",
    "LAN": "LA1",
    "LAS": "LA2",
    "KR": "KR",
    "JP": "JP1",
    "EUNE": "EUN1",
    "EUW": "EUW1",
    "TR": "TR1",
    "RU": "RU",
    "OCE": "OC1",
    "PH2": "PH2",
    "SG2": "SG2",
    "TH2": "TH2",
    "TW2": "TW2",
    "VN2": "VN2",
}

def get_match_string(region: str, match_id: str) -> str:
    return f"{server_string[region]}_{match_id}"