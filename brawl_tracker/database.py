
import sqlite3

db_name = 'brawl.db'

def get_connection():
    return sqlite3.connect(db_name)
    
def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        #daily player snapshot
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS player_snapshots(
                        date TEXT PRIMARY KEY,
                        trophies INTEGER,
                        highest_trophies INTEGER,
                        solo_wins INTEGER,
                        duo_wins INTEGER,
                        trio_wins INTEGER
                    )
                    ''')
        #battle history
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS battles(
                        battle_time TEXT PRIMARY_KEY,
                        mode TEXT,
                        result TEXT,
                        trophies_change INTEGER
                    )
                    ''')
        #per brawler snapshot

        conn.commit()