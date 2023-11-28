from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # A simple HTML file with your WebSocket client

@socketio.on('audio_file')
def handle_audio_file(data_url):
    print("Received audio file")
    # Process the audio file here
    socketio.emit('audio_response', 'Audio file received and processed')

if __name__ == '__main__':
    socketio.run(app, debug=True)
