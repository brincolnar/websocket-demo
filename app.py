import base64
from flask import Flask, render_template
from flask_socketio import SocketIO
import os 
import openai
from dotenv import find_dotenv, load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return render_template('index.html')  # A simple HTML file with your WebSocket client

@socketio.on('audio_file')
def handle_audio_file(data_url):
    print("Received audio file")

    # Extract the base64 encoded audio data from the data URL
    header, encoded = data_url.split(",", 1)
    audio_data = base64.b64decode(encoded)

    # Specify a file path to save the audio
    file_path = "received_audio.wav"  # or any other appropriate file extension

    # Write the audio data to a file
    with open(file_path, 'wb') as file:
        file.write(audio_data)

    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    text = transcript['text']

    # Remove the temporary audio file if needed
    os.remove(file_path)


    print(f"Audio file saved as {file_path}")
    socketio.emit('audio_response', f'Audio file transcript: {text}')

if __name__ == '__main__':
    socketio.run(app, debug=True)
