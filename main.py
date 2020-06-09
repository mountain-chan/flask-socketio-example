from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import request

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
users = {}


@socketio.on('connect')
def test_connect():
    print('[CONNECTED] ' + request.sid)


@socketio.on('disconnect')
def test_disconnect():
    print('[DISCONNECTED] ' + request.sid)


@socketio.on('login')
def login(username):
    users[username] = request.sid
    print(username + ' Login')


@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)


@socketio.on('chat_private')
def chat_private(data):
    receive_session_id = users[data['username']]
    message = data['message']
    emit('new_private_msg', message, room=receive_session_id)


@socketio.on('chat_group')
def chat_group(data):
    room = data['room']
    sender = data['username']
    message = sender + ': ' + data['message']
    emit('new_group_msg', message, room=room)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)


@socketio.on('join2', namespace='/message2')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


@socketio.on('message2', namespace='/message2')
def on_message2(msg):
    emit('message2', msg, room='msg2')


if __name__ == '__main__':
    socketio.run(app)
