from flask import Flask
from flask import request
from flask import render_template, send_from_directory
import base64
import memory_llm
from langchain.load.dump import dumps
from openai import OpenAI

import os
app = Flask(__name__)

OPENAI_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_KEY)

system_message = f"""
Eres un asistente virtual de nuestro instituto. Los clientes te harán preguntas sobre cursos y sus precios.\n\n

Ubicación de la institución: Av. América Este. Edificio Ferrara Piso 1 Oficina 2\n
Ciudad de Cochabamba, Bolivia\n
Precio del curso de Python: 200 Bs\n
Precio del curso de Robótica: 300 Bs\n

Inicio del curso de Python: 04 de septiembre\n
Inicio del curso de Robótica: 11 de septiembre\n
Sólo tenemos esos cursos por ahora\n
También vendemos kits de robótica educativa.\n

Si no conoces la respuesta, que manden un correo a info.cebtic@gmail.com
"""

@app.route('/stateless-chat', methods=['GET'])
def stateless_chat():
    return render_template('stateless_chat.html')

@app.route('/memory-chat', methods=['GET'])
def memory_chat():
    return render_template('memory_chat.html')

@app.route('/audio-chat', methods=['GET'])
def audio_chat():
    return render_template('audio_chat.html')

@app.route('/image-generator', methods=['GET'])
def image_generator():
    return render_template('image_generating_chat.html')

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

    transcript = client.audio.transcriptions.create(file=audio_file, model='whisper-1')
    
    return {'text': transcript.text}

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['data']
    response = client.chat.completions.create(model="ft:gpt-3.5-turbo-0613:personal:umss-assistant:8pRwESDk",
                                              temperature=1,
                                              messages = [
                                                    {"role": "system", "content": system_message},
                                                    {"role": "user", "content": prompt}
                                              ])
    print(response.choices)
    return {'content': response.choices[0].message.content}

@app.route('/chatmemory', methods=['POST'])
def chat_with_memory():
    prompt = request.json['data']
    result = memory_llm.store_conversation(prompt)
    print(result)
    return dumps(result)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    prompt = request.json['data']
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return {'url': response.data[0].url}

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
