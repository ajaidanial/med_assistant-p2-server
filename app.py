from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretasdsad!'
socketio = SocketIO(app)


@app.route('/')
def home():
    return "Hello World"

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

# to receive
@socketio.on('event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print('received my event: ' + data)
    # to send
    socketio.emit('response', "output", callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app)