import sqlite3
import yaml

def get_db_name():
    try:
        with open("config.yaml", "r") as cfg:
            contents = yaml.safe_load(cfg)
            name = contents["database_name"]
            return name
    except:
        print("[!] NO CONFIG FILE FOUND")
        quit()

class Database:
    def __init__(self,name):
        self.name = name
    
    def make(self):
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS songs(
                    sid int PRIMARY KEY,
                    source TEXT,
                    music_path TEXT
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS queues(
                    qid INT PRIMARY KEY,
                    count INT,
                    song_id INT,
                    FOREIGN KEY(song_id) REFERENCES songs(sid)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    uid INT PRIMARY KEY,
                    username TEXT,
                    phash TEXT
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS rooms(
                    rid INT PRIMARY KEY,
                    capacity INT,
                    queue INT,
                    room_owner INT,
                    chat_id INT,
                    FOREIGN KEY (queue) REFERENCES queue(qid),
                    FOREIGN KEY (room_owner) REFERENCES users(uid)
                    FOREIGN KEY (chat_id) REFERENCES chats(cid)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS chats(
                    cid INT PRIMARY KEY,
                    user_id INT,
                    message TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(uid)
                    )""")
        con.commit()
        con.close()
    
    