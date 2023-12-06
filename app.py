import base64
from flask import Flask, render_template
from flask_socketio import SocketIO
import os 
import openai
from dotenv import find_dotenv, load_dotenv
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_LABS_API_KEY=os.getenv("ELEVEN_LABS_API_KEY")

openai.api_key = OPENAI_API_KEY

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": ELEVEN_LABS_API_KEY
}
data = {
  "text": "<placeholder>",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

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

    data["text"] = text
    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    # Convert the generated audio file to a data URL and send it back
    with open('output.mp3', 'rb') as audio_file:
        audio_data = audio_file.read()
        audio_data_url = "data:audio/mpeg;base64," + base64.b64encode(audio_data).decode()
        socketio.emit('audio_file_response', audio_data_url)

    '''
    print(f"Audio file saved as {file_path}")
    socketio.emit('audio_response', f'Audio file transcript: {text}')
    '''
if __name__ == '__main__':
    socketio.run(app, debug=True)
