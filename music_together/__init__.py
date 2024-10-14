import sqlite3
from music_together.func import Database, get_db_name
import os
import secrets

def start():
    db = Database(get_db_name())
    db.make()
    print("[+] Database created successfully.")

    if "config.yaml" not in os.listdir():
        with open("config.yaml", "w+") as f:
            f.write(f"""database_name: "database.db" # default: database.db\nsecret: "{secrets.token_hex(20)}" """)

    from music_together.routes import app
    app.run(host="0.0.0.0", port="5000", debug=True)