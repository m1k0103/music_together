from flask import Flask, render_template, redirect, url_for, request, session
from music_together.func import Database, get_db_name, get_secret

app = Flask(__name__)
DB = Database(get_db_name())

app.secret_key = get_secret()

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_conf = request.form["password-conf"]
        if password == password_conf and DB.is_user_taken(username):
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
        pass # do stuff here
    pass

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    pass

@app.route("/get_rooms") # will be displayed on the index page
def get_rooms():
    pass

@app.route("/create_room")
def create_room():
    pass

@app.route("/delete_room")
def delete_room():
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
