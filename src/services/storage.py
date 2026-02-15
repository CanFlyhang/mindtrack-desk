import sqlite3
import datetime
import os

class DataManager:
    def __init__(self, db_path="logs/history.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                window_title TEXT,
                summary TEXT,
                image_path TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_record(self, window_title, summary, image_path):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO history (timestamp, window_title, summary, image_path)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, window_title, summary, image_path))
        conn.commit()
        conn.close()

    def get_recent_records(self, limit=50):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM history ORDER BY id DESC LIMIT ?', (limit,))
        records = cursor.fetchall()
        conn.close()
        return records
