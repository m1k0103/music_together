from flask import Flask, render_template, redirect, url_for, request, session
from music_together.func import Database, get_db_name, get_secret

# Initialized Flask and Database classes
app = Flask(__name__)
DB = Database(get_db_name())

# Gets secret key stored in config.yaml
app.secret_key = get_secret()

# Route and behaviour for the index page. (aka homepage)
@app.route("/",methods=["GET","POST"])
def index():
    error = ""
    if request.method == "GET":
        all_rooms = DB.get_all_rooms_info()
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
            return redirect(url_for("index"))
        else:
            return redirect(url_for("signup"))
        

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
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    pass

@app.route("/create_room")
def create_room():
    pass

@app.route("/delete_room")
def delete_room():
    pass

@app.route("/join_room")
def join_room():
    pass

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

@app.route("/get_room_chat")
def get_room_chat():
    pass

@app.route("/send_message")
def send_room_chat_message():
    pass
