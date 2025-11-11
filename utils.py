import sqlite3
from flask import g
DATABASE = "main.db"

LOGS_DIRECTORY = "/logs"
REDIRECT_DIRECTORY = "/redirect"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


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