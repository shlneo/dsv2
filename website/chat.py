from flask import Blueprint, session
from flask_socketio import SocketIO, join_room, leave_room, emit
import uuid
from website import socketio

chat = Blueprint('chat', __name__)

room_users = {}

def generate_unique_user_id():
    """Генерирует уникальный идентификатор пользователя."""
    return str(uuid.uuid4()) 

@socketio.on('connect')
def handle_connect():
    if 'user_id' not in session:
        session['user_id'] = generate_unique_user_id()

    user_id = session.get('user_id')
    print(f"User {user_id} connected")
    emit('user_connected', {'message': 'A user has connected!'})

@socketio.on('disconnect')
def handle_disconnect():
    user_id = session.get('user_id')
    if not user_id:
        print("No user_id found in session during disconnect.")
        return

    for room, users in room_users.items():
        if user_id in users:
            users.remove(user_id)
            leave_room(room)
            emit('leave_room_announcement', {'message': f'{user_id} has left the room {room}'}, room=room)
            print(f"User {user_id} disconnected and left room {room}")

@socketio.on('join')
def on_join(data):
    username = data['user']
    room = data['room']
    user_id = session.get('user_id')

    if room not in room_users:
        room_users[room] = []

    if user_id not in room_users[room]:
        room_users[room].append(user_id)

    join_room(room)
    
    emit('join_room_announcement', {'message': f'{username} has joined the room {room}'}, room=room)
    print(f"{username} (ID: {user_id}) has joined the room {room}")

@socketio.on('leave')
def on_leave(data):
    username = data['user']
    room = data['room']
    user_id = session.get('user_id')

    if room in room_users and user_id in room_users[room]:
        room_users[room].remove(user_id)

    leave_room(room)

    emit('leave_room_announcement', {'message': f'{username} has left the room {room}'}, room=room)
    print(f"{username} (ID: {user_id}) has left the room {room}")

@socketio.on('get_room_participants')
def get_room_participants(data):
    room = data['room']
    participants = room_users.get(room, [])
    
    emit('room_participants', {'room': room, 'participants': participants})
