import sqlite3
import pandas as pd
import streamlit as st

DB_NAME = "brawl.db"

def load_snapshots():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT * from player_snapshots order by date", conn
    )
    conn.close()
    return df

def load_battles(limit = 20):
    conn = sqlite3.connect((DB_NAME))
    df = pd.read_sql_query(
        f"""
            SELECT battle_time, mode, result, trophies_change
            from battles
            ORDER BY battle_time DESC
            LIMIT {limit}
        """,
         conn)
    conn.close()
    return  df

st.set_page_config(page_title="Brawl Stars Progress", layout="wide")

st.title("📊 Brawl Stars Progress Dashboard")

# ------SNAPSHOTS ------
snapshots = load_snapshots()

if snapshots.empty:
    st.warning("No snapshots data yet. Run tracker.py first")
    st.stop()

snapshots["date"] = pd.to_datetime(snapshots["date"])
snapshots["daily_gain"] = snapshots["trophies"].diff()


# ----METRICS----
col1, col2, col3 = st.columns(3)
col1.metric("🏆 Current Trophies", snapshots.iloc[-1]["trophies"])
col2.metric("📈 Highest Trophies", snapshots.iloc[-1]["highest_trophies"])
col3.metric("📅 Days Tracked", len(snapshots))

st.divider()

# ----Trophy Graph----
st.subheader("🏆 Trophy Progress Over Time")
st.line_chart(
    snapshots.set_index("date")["trophies"]
)

#----Daily Gains ----
st.subheader("📈 Daily Trophy Gain")
st.bar_chart(
    snapshots.set_index("date")["daily_gain"]
)

#----Battles----
st.subheader("⚔️ Recent Battles")
battles = load_battles(25)

st.dataframe(
    battles,
    width='stretch'
)