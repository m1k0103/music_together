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

def is_session_valid(session):
    if "authed" in session and session["authed"]:
        return True
    else:
        return False

class Database:
    def __init__(self,name):
        self.name = name

    def db_connect(self):
        con = sqlite3.connect(self.name)
        cur = con.cursor()
        return con,cur

    def make(self):
        con,cur = self.db_connect()
        cur.execute("""CREATE TABLE IF NOT EXISTS songs(
                    sid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    source TEXT,
                    music_path TEXT
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS queues(
                    associated_rid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    count INT,
                    song_id INT,
                    FOREIGN KEY(song_id) REFERENCES songs(sid)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    uid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    username TEXT,
                    phash TEXT,
                    connected_to_rid INTEGER
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS rooms(
                    rid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT,
                    password TEXT,
                    capacity INT,
                    room_owner INT,
                    FOREIGN KEY (room_owner) REFERENCES users(uid)
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS chats(
                    room_id INT,
                    user_id INT,
                    message TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(uid),
                    FOREIGN KEY (room_id) REFERENCES rooms(rid)
                    )""")
        con.commit()
        con.close()
    
    def is_user_taken(self,username):
        con,cur = self.db_connect()
        try:
            result = cur.execute("SELECT username FROM users WHERE username=?", [username]).fetchone()[0]
            con.close()
            return True
        except:
            con.close()
            return False
        
    def create_user(self,username,password):
        phash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        con,cur = self.db_connect()
        cur.execute("INSERT INTO users(username,phash) VALUES (?,?)",[username,phash])
        con.commit()
        con.close()

    def validate_password(self,username,password):
        input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        con,cur = self.db_connect()
        stored_hash = cur.execute("SELECT phash FROM users WHERE username=?",[username]).fetchone()[0]
        con.close()
        if str(input_hash) == str(stored_hash):
            return True
        else:
            return False

    def get_all_rooms_info(self):
        con,cur = self.db_connect()
        result = [list(tup) for tup in cur.execute("SELECT rid,name,password,capacity FROM rooms").fetchall()]
        return result
        
    def create_room(self,rname,rpass,capacity,user_creating):
        con,cur = self.db_connect()
        cur.execute("INSERT INTO rooms(name,password,capacity,room_owner) VALUES (?,?,?,(SELECT uid FROM users WHERE username=?))",[rname,rpass,capacity,user_creating])
        con.commit()
        room_id = cur.execute("SELECT rid FROM rooms WHERE name=? AND password=?",[rname,rpass]).fetchall()[0][0]
        con.close()
        return room_id
    
    def send_message(self,user,message):
        con,cur = self.db_connect()
        cur.execute("INSERT INTO chats()")
    
    def join_room(self,room_id,user,provided_pass):
        con,cur = self.db_connect()
        room_pass = cur.execute("SELECT password FROM rooms WHERE rid=?",[room_id]).fetchone()[0]
        room_cap = cur.execute("SELECT capacity FROM rooms WHERE rid=?",[room_id]).fetchone()[0]
        connected_users = len(cur.execute("SELECT username FROM users WHERE connected_to_rid=?",[room_id]).fetchall())
        if connected_users >= room_cap:
            return False
        else:
            if provided_pass != room_pass:
                return False
            else:
                cur.execute("UPDATE users SET connected_to_rid=? WHERE username=?",[room_id,user])
                con.commit()
                con.close()
                return True
            