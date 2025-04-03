from flask_socketio import  join_room, leave_room, emit
from flask import session as flask_session
from main import socketio

rooms = {}

@socketio.on('join_room')
def handle_join(data):
    username = flask_session["auth_state"]["sub"]
    room = data['room']
    join_room(room)
    if room not in rooms:
        rooms[room] = {"users": [], "stories": [], "votes": {}}
    rooms[room]['users'].append(username)
    emit('room_update', rooms[room], room=room)

@socketio.on('leave_room')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    rooms[room]['users'].remove(username)
    emit('room_update', rooms[room], room=room)

@socketio.on('vote')
def handle_vote(data):
    room = data['room']
    story_id = data['storyId']
    username = data['username']
    points = data['points']
    rooms[room]['votes'][username] = points
    emit('vote_update', rooms[room]['votes'], room=room)

@socketio.on('finalize_story')
def handle_finalize(data):
    room = data['room']
    story_id = data['storyId']
    points = data['points']
    # Notify all users that the story has been finalized
    emit('story_finalized', {"storyId": story_id, "points": points}, room=room)
    # Call the update API for persistence
    # Replace with your API request logic
    print(f"Finalized story {story_id} with {points} points")

@socketio.on('delete_room')
def handle_delete_room(data):
    room = data['room']
    if room in rooms:
        del rooms[room]  # Remove the room from the in-memory store
        emit('room_deleted', {"room": room}, broadcast=True)  # Notify all clients
    else:
        emit('error', {"message": f"Room {room} does not exist."})
