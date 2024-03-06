import requests as r

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en-CA;q=0.9,en;q=0.8,ru-RU;q=0.7,ru;q=0.6,ko-KR;q=0.5,ko;q=0.4",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

def get_account_by_riot_id(game_name: str, tag_line: str, api_key: str) -> dict:
    # There are three routing values for account-v1; americas, asia, and europe. You can query for any account in any region. We recommend using the nearest cluster.
    response = r.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}", headers=headers)
    
    response.raise_for_status()
    
    return response.json()

def get_account_by_puuid(puuid: str, api_key: str) -> dict:
    response = r.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={api_key}", headers=headers)
    
    response.raise_for_status()
    
    return response.json()