from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask import request

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
users = {}


# The connection event handler can return False to reject the connection, or it can also raise ConectionRefusedError
@socketio.on('connect')
def test_connect():
    print('[CONNECTED] ' + request.sid)


# Disconnect event when client run socket.disconnect();
@socketio.on('disconnect')
def test_disconnect():
    print('[DISCONNECTED] ' + request.sid)


# a user when connect to this socket will have a session ID of the connection which can be obtained from request.sid
# this function will store all users in a dictionary with username and the session ID of the connection
@socketio.on('login')
def login(username):
    users[username] = request.sid
    print(username + ' Login')


# broadcast=True When a message is sent with the broadcast option enabled, all clients connected
# to the namespace receive it, including the sender. When namespaces are not used, the clients
# connected to the global namespace receive the message
@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)


# a session ID of the connection is a room contain this user, this function will get session id of the receiver user
# from dictionary users, then emit event new_private_msg with parameter room=receive_session_id
@socketio.on('chat_private')
def chat_private(data):
    receive_session_id = users[data['username']]
    message = data['message']
    emit('new_private_msg', message, room=receive_session_id)


# room=room all clients join this room will receive it
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


# room=room all clients join this room will receive it
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