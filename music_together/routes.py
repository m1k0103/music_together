from flask import Flask, render_template, redirect, url_for, request, session
from music_together.func import Database, get_db_name, get_secret, is_session_valid
from datetime import datetime

# TODO
#   - figure out a way to display any errors
#   - do more coding than soly (im watching you...)
#   - When making a route, finish the func that it will need
#   - Other?????
#   - Write a proper readme

# Initialized Flask and Database classes
app = Flask(__name__)
DB = Database(get_db_name())

# Gets secret key stored in config.yaml
app.secret_key = get_secret()

# Error variable. CURRENTLY DOESNT WORK.
global error
error = ""

# Route and behaviour for the index page. (aka homepage)
@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "GET":
        session["room"] = ""
        all_rooms = DB.get_all_rooms_info()
        print(f"error: {error}")
        return render_template("index.html", all_rooms=all_rooms,error=error) #pass all_rooms into template 
    elif request.method == "POST":
        pass

# Route and behaviours for the signup page.
@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_conf = request.form["password-conf"]
        if password == password_conf and DB.is_user_taken(username) == False:
            DB.create_user(username,password)
            session["username"] = username
            session["authed"] = True
            return redirect(url_for("index"))
        else:
            return redirect(url_for("signup"))
        
# Login route. Handles rendering the login page and the login POST request
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if DB.is_user_taken(username) == True and DB.validate_password(username,password) == True:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    
# Clears session of the user.
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    pass

# Route that allows a room to be created.
@app.route("/create_room",methods=["POST"])
def create_room():
    if request.method == "POST":
        rname = request.form["room_name"]
        rpassword = request.form["room_password"]
        capacity = int(request.form["capacity"])
        if is_session_valid(session) == False:
            print("session invalid")
            return redirect(url_for("index"))
        else:
            DB.create_room(rname,rpassword,capacity,session["username"])
            print("room created")
            return redirect(url_for("index"))

@app.route("/room",methods=["GET","POST"])
def room():
    if request.method == "GET":
        if session["room"] != "":
            room_id = session["room"]
            return render_template("room.html", room_id=room_id)
        else:
            return redirect(url_for("index"))


@app.route("/delete_room")
def delete_room():
    pass

@app.route("/join_room",methods=["POST"])
def join_room():
    if request.method == "POST":
        try: # if room is public
            room_password = request.form["room-password-input"]
        except: 
            room_password = ""
        finally:
            room_id = request.form["room_id"]
            joined = DB.join_room(room_id,session["username"],room_password)
            if joined == True:
                session["room"] = room_id
                return redirect(url_for("room"))
            else:
                return redirect(url_for("index")) 
        
@app.route("/leave_current_room",methods=["POST"])
def leave_current_room():
    session["room"] = ""
    DB.leave_room(session["username"])
    return redirect(url_for("index"))

@app.route("/change_room_name")
def change_room_name():
    pass

@app.route("/update_room_current_song")
def update_room_current_song():
    pass

@app.route("/add_to_room_queue")
def add_to_room_queue():
    pass

@app.route("/remove_from_room_queue")
def remove_from_room_queue():
    pass

@app.route("/get_room_chat",methods=["GET"])
def get_room_chat():
    rid = session["room"]
    messages = DB.get_last_messages(20,rid)
    return render_template("messages.html",data=messages) # finish above func first


@app.route("/send_message",methods=["POST"])
def send_message():
    if request.method == "POST":
        rid = request.form["room_id"]
        user = session["username"]
        message = request.form["message"]
        time = str(datetime.now()).split(" ")[1].split(".")[0]
        DB.send_message(rid,user,message,time)
        return redirect(url_for("room"))
    
 # room_id, user_id, message