import sqlite3
import os

DB_PATH = "data/watchdog.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        url TEXT,
        timestamp TEXT,
        screenshot_path TEXT
    )''')
    conn.commit()
    conn.close()

def save_snapshot(name, url, timestamp, screenshot_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO snapshots (name, url, timestamp, screenshot_path) VALUES (?, ?, ?, ?)",
              (name, url, timestamp, screenshot_path))
    conn.commit()
    conn.close()

def get_latest_snapshots():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, MAX(timestamp), screenshot_path FROM snapshots GROUP BY name")
    rows = c.fetchall()
    conn.close()
    return rows

def get_history_for(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, screenshot_path FROM snapshots WHERE name=? ORDER BY timestamp DESC", (name,))
    rows = c.fetchall()
    conn.close()
    return rows
