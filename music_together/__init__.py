import sqlite3
from music_together.func import Database, get_db_name

def start():
    db = Database(get_db_name())
    db.make()
    print("[+] Database created successfully.")