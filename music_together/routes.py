from flask import Flask

app = Flask(__name__)


app.route("/")
def index():
    pass

@app.route("/login")
def login():
    pass

@app.route("/logout")
def logout():
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

