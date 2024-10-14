import sqlite3
from music_together.func import Database, get_db_name
import os

def start():
    db = Database(get_db_name())
    db.make()
    print("[+] Database created successfully.")

    from music_together.routes import app
    app.run(host="0.0.0.0", port="5000", debug=True)