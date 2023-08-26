from flask import Flask
from flask import request
from flask import render_template, send_from_directory
import base64
import openai
app = Flask(__name__)

OPENAI_KEY = "<Tu llave de OpenAI>"
OPENAI_API_URL = "https://api.openai.com/v1"
openai.api_key = OPENAI_KEY
openai.api_base = OPENAI_API_URL

system_message = f"""
Eres un asistente virtual de la Universidad Autonoma Gabriel Rene Moreno. \
Los estudiantes te harán preguntas sobre la universidad y debes responder en base a la \
informacion que ahora te proporcionamos \

Año de fundacion: 1880 \
es una universidad publica de Bolivia \
tiene 18 facultades \
tiene 60 carreras \
se debe rendir un examen para ingresar \
tambien es posible a través de un curso preuniversitario
"""

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/resources/<path:path>', methods=['GET'])
def resources(path):
    return send_from_directory('resources', path)

@app.route('/transcribe', methods=['POST'])
def post_audio_file():
    file = request.json['data']

    decoded_bytes = base64.b64decode(file)
    with open('music.webm', 'wb') as wav_file:
        wav_file.write(decoded_bytes)
        
    audio_file = open('music.webm', "rb")

    transcript = openai.Audio.transcribe('whisper-1',audio_file, OPENAI_KEY)
    
    return transcript

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['data']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
