from flask import Flask, render_template, request
from flask_socketio import SocketIO
import base64
import openai
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


@app.route('/')
def index():
    return render_template('index.html')  # A simple HTML file with your WebSocket client

@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    socketio.send("Echo: " + message)  # Echoing received message

@socketio.on('mp3_file')
def handle_mp3(data_url):

    print("/mp3_file")

    # Decode the base64 data
    header, encoded = data_url.split(",", 1)
    file_data = base64.b64decode(encoded)

    # Save the MP3 file temporarily
    with open("temp.mp3", "wb") as f:
        f.write(file_data)

    # Use Whisper for transcription
    with open("temp.mp3", "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    transcript = transcript['text']

    # Send the transcript back to the client
    socketio.send(transcript)

if __name__ == '__main__':
    socketio.run(app, debug=True)
