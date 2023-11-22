from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # A simple HTML file with your WebSocket client

@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    socketio.send("Echo: " + message)  # Echoing received message

if __name__ == '__main__':
    socketio.run(app, debug=True)
