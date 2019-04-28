from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretasdsad!'
socketio = SocketIO(app)


@app.route('/')
def home():
    return "Hello World"

def messageReceived(methods=['GET', 'POST']):
    pass

# to receive
@socketio.on('event')
def handle_my_custom_event(data, methods=['GET', 'POST']):
    print('received my event: ' + data)
    # to send
    socketio.emit('response', "output", callback=messageReceived)

# dialogflow incomming
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)['result']['resolvedQuery'].lower().replace("and", ",").strip()
    out = prediction(data)
    # send
    socketio.emit('response', out, callback=messageReceived)
    # TODO return to reply
    reply = {
        "speech": ",".join(out)
    }
    return jsonify(reply)
# TODO: add 'ngrok http 5000'

# receive and send to bot


if __name__ == '__main__':
    socketio.run(app)