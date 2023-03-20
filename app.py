import correo
from flask import Flask, request, jsonify
from flask_cors import CORS
from dateutil.parser import parse
from googletrans import Translator
import time
import pprint
import threading
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
evento = {}
evento['para'] = ''
evento['asunto'] = ''
evento['fecha'] = ''
evento['estado'] = False

eventoaux = {}
eventoaux['para'] = ''
eventoaux['asunto'] = ''
eventoaux['fecha'] = ''

def send_email(eventos):
    for e in eventos:
        if e['estado'] == False and e['fecha'] <= (datetime.now() + timedelta(days=1)):
            correo.enviar(e['para'], e['asunto'], 'Tienes una {} el dia {}'.format(e['asunto'], str(e['fecha'])))
            #print('Tienes una {} el dia {}'.format(e['asunto'], str(e['fecha'])))
            e['estado'] = True

def mi_funcion_constante():
    eventos = []
    while True:
        if eventoaux['fecha'] != evento['fecha'] or eventoaux['asunto'] != evento['asunto'] or eventoaux['para'] != evento['para']:
            eventoaux['fecha'] = evento['fecha']
            eventoaux['asunto'] = evento['asunto']
            eventoaux['para'] = evento['para']
            eventos.append(
                {
                    'fecha': evento['fecha'],
                    'asunto': evento['asunto'],
                    'para': evento['para'],
                    'estado': evento['estado']
                }
            )
        # Lógica que se ejecuta constantemente
        send_email(eventos)
        time.sleep(1)

@app.before_first_request
def iniciar_funcion_constante():
    t = threading.Thread(target=mi_funcion_constante)
    t.start()

def tradu(text):
    traductor = Translator()
    texto_ingles = traductor.translate(text, src='es', dest='en').text
    return texto_ingles
    
@app.route('/new', methods = ['POST'])
def add_event():
    evento['para'] = request.json["para"]
    evento['asunto'] = request.json["asunto"]
    evento['fecha'] = parse(tradu(request.json["fecha"]), fuzzy=True)
    print(evento['fecha'])
    if evento: 
        return 'Nuevo evento'
    else:
        return "Error al recibir el mensaje"

if __name__ == '__main__':
    app.run(debug=True)