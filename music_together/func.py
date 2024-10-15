import sqlite3
import yaml
import hashlib

def get_db_name():
    try:
        with open("config.yaml", "r") as cfg:
            contents = yaml.safe_load(cfg)
            name = contents["database_name"]
            return name
    except:
        print("[!] NO CONFIG FILE FOUND")
        quit()

def get_secret():
    try:
        with open("config.yaml", "r") as cfg:
            contents = yaml.safe_load(cfg)
            secret = contents["secret"]
            return secret
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
                    sid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    source TEXT,
                    music_path TEXT
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS queues(
                    qid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    count INT,
                    song_id INT,
                    FOREIGN KEY(song_id) REFERENCES songs(sid)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    uid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    username TEXT,
                    phash TEXT
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS rooms(
                    rid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    capacity INT,
                    queue INT,
                    room_owner INT,
                    chat_id INT,
                    FOREIGN KEY (queue) REFERENCES queue(qid),
                    FOREIGN KEY (room_owner) REFERENCES users(uid)
                    FOREIGN KEY (chat_id) REFERENCES chats(cid)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS chats(
                    cid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    user_id INT,
                    message TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(uid)
                    )""")
        con.commit()
        con.close()
    
    def is_user_taken(self,username):
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        try:
            result = cur.execute("SELECT username FROM users WHERE username=?", [username]).fetchone()[0]
            return True
        except:
            return False
        
    def create_user(self,username,password):
        phash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        cur.execute("INSERT INTO users(username,phash) VALUES (?,?)",[username,phash])
        con.commit()
        con.close()

    def validate_password(self,username,password):
        input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        stored_hash = cur.execute("SELECT phash FROM users WHERE username=?",[username]).fetchone()[0]
        con.close()
        if str(input_hash) == str(stored_hash):
            return True
        else:
            return False