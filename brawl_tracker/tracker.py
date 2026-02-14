import requests
from urllib.parse import quote
from config import API_KEY, player_tag
from datetime import date
from database import init_db, get_connection

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_player():
    url = f"https://api.brawlstars.com/v1/players/{quote(player_tag)}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def getbattle_log():
    url = f"https://api.brawlstars.com/v1/players/{quote(player_tag)}/battlelog"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["items"]

def save_snapshot(player):
    today = date.today().isoformat()

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO player_snapshots(date, trophies, highest_trophies, solo_wins, duo_wins, trio_wins)
                    VALUES (?, ?, ?, ?, ?, ?)
        """,(
        today,
        player['trophies'],
        player["highestTrophies"],
        player['soloVictories'],
        player['duoVictories'],
        player['3vs3Victories'],
        ))
        conn.commit()


def save_battles(battles):
    with get_connection() as conn:
        cur = conn.cursor()
        for b in battles:
            battle_time = b["battleTime"]
            mode = b["event"]["mode"]
            result = b["battle"].get("result")
            trophies_change = b["battle"].get("trophyChange")
            cur.execute("""
                INSERT OR IGNORE INTO battles(battle_time, mode, result, trophies_change)
                VALUES (?, ?, ?, ?)
            """, (
                battle_time,
                mode,
                result,
                trophies_change
            ))
        conn.commit()


if __name__ == "__main__":
    init_db()

    player = get_player()
    battles = getbattle_log()

    print("Player:", player["name"])
    print("Trophies:", player["trophies"])
    print("Recent battles:", len(battles))

    save_snapshot(player)
    save_battles(battles)

    print("Saved daily snapshot + battles")