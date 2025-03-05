# khadijas code for chatbox

from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from flask_socketio import emit, join_room, leave_room
from extension import db
from models.user import UserModel

chat = Blueprint("chat", __name__, url_prefix="/chat")

# Dictionary to store active users and their Socket.IO session IDs
active_users = {}

def init_socketio(socketio):
    @socketio.on('connect')
    def handle_connect():
        """Handles new Socket.IO connections."""
        user_id = session.get('user_id')
        if user_id:
            # Store the user's Socket.IO session ID
            active_users[user_id] = request.sid
            # Broadcast the updated user list to all clients
            emit('update_user_list', list(active_users.keys()), broadcast=True)

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handles Socket.IO disconnections."""
        user_id = session.get('user_id')
        if user_id and user_id in active_users:
            # Remove the user from the active users list
            del active_users[user_id]
            # Broadcast the updated user list to all clients
            emit('update_user_list', list(active_users.keys()), broadcast=True)

    @socketio.on('join_room')
    def handle_join_room(data):
        """Handles joining a chat room."""
        room = data['room']
        join_room(room)
        emit('room_joined', {'room': room})
        print(f"User joined room: {room}")

    @socketio.on('leave_room')
    def handle_leave_room(data):
        """Handles leaving a chat room."""
        room = data['room']
        leave_room(room)
        emit('room_left', {'room': room})

    @socketio.on('send_message')
    def handle_send_message(data):
        """Handles sending a message to a room."""
        room = data['room']
        message = data['message']
        sender_id = session.get('user_id')
        sender = UserModel.query.get(sender_id)
        print(f"Message received in room {room}: {message} from {sender.username}")  # Debugging
        # Emit the message to the recipient's room
        emit('receive_message', {
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender.username
        }, room=room)
        
        # Additionally, send the message to the sender’s room (so they can see it as well)
        emit('receive_message', {
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender.username
        }, room=sender_id)

@chat.route('/')
def chat_home():
    """Renders the chat page."""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    return render_template('messages.html')

@chat.route('/get_users')
def get_users():
    """Returns a JSON list of all users excluding the logged-in user."""
    user_id = session.get('user_id')
    users = UserModel.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users if user.id != user_id]
    return jsonify(user_list)

@chat.route('/test')
def test_route():
    return "Chat blueprint is working!"
