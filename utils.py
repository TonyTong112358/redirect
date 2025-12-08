import sqlite3
from flask import g
DATABASE = "main.db"

LOGS_DIRECTORY = "/log"
REDIRECT_DIRECTORY = "/redirect"

def get_db(as_dict = False):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        if as_dict:
            db.row_factory = sqlite3.Row
    return db


def store_logs(timestamp, ip_address, request_method, request_headers, request_body, request_arguments, request_path):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO logs (timestamp, ip_address, request_method, request_headers, request_body, request_arguments, request_path) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (timestamp, ip_address, request_method, request_headers, request_body, request_arguments, request_path))
    db.execute("PRAGMA journal_mode=WAL;")

    db.commit()


def get_logs(count = 100):
    db = get_db(as_dict=True)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (count,))
    logs = cursor.fetchall()
    return logs

def get_redirect_url():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT url FROM redirect_url WHERE id = 1")
    url = cursor.fetchone()
    return url[0] if url else None
def load_panel_value():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT url FROM redirect_url WHERE id = 1")
    url = cursor.fetchone()
    cursor.execute(f"SELECT header, directory, body, status_code FROM Response WHERE id = 1")
    response = cursor.fetchone()

    result = {
        "url": url[0] if url else None,
        "header": response[0] if response else None,
        "path": response[1] if response else None,
        "body": response[2] if response else None,
        "status_code": response[3] if response else None
    }
    return result