from music_together import start

if __name__ == "__main__":
    start()

#todo:
# - add chat to room ✓
#   + maybe experiment with a "flask listener" or something to reduce amount of requests send to server?? nah
# - test passwords with rooms with multiple clients
# - test connecting without valid user
# - make it so that there is a "leave room" button.
#   + no navbar, and redirecting user to room until theu leave.
#   + cant leave room or navigate any other page. will have to add to base.html
# - start progress on the actual music part
#   + figure out a way to sync two client's musics together (aj aj aj...)
