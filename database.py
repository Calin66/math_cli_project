
import sqlite3
from datetime import datetime

def get_connection():
    conn = sqlite3.connect('requests.db')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation TEXT NOT NULL,
        input_data TEXT NOT NULL,
        result TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    return conn

def save_request(operation: str, input_data: str, result: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO requests (operation, input_data, result, created_at) VALUES (?, ?, ?, ?)",
        (operation, input_data, result, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
