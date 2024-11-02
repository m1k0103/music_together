from music_together.func import Database, get_db_name
import os
import secrets

def start():

    if "config.yml" not in os.listdir():
        f = open("config.yml", "w+")
        f.write(f"""database_name: "database.db" #default: database.db\nsecret: "{secrets.token_hex(20)}" """)
        f.close()
    else:
        pass

    db = Database(get_db_name())
    db.make()
    print("[+] Database created successfully.")



    from music_together.routes import app
    app.run(host="0.0.0.0", port="5000", debug=True)