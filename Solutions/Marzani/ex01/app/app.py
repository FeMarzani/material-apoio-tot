# Importando bibliotecas

from flask import Flask, jsonify
from threading import Thread
from dotenv import load_dotenv
from utils.listener import ProcessSQSListener
from utils.write_env import *


app = Flask(__name__)

# Criando rota de /health
@app.route('/health', methods=['GET'])
def health_check():

    URL = os.getenv('URL')

    # Formatando resposta da rota
    resposta = requests.get(URL)
    data = json.loads(resposta.text)
    status_code = resposta.status_code

    return {
        "statusCode": status_code,
        "body": data
    }

@app.route('/', methods=['GET'])
def receive_message():
    return jsonify({'Application': 'Running Polling'}), 200


# Função de execução do listener.
def process():

    process_listener = ProcessSQSListener(SQS_IN_NAME,
                                          endpoint_name=ENDPOINT_URL,
                                          aws_access_key=KEY_ID,
                                          aws_secret_key=ACCESS_KEY,
                                          queue_url=SQS_IN,
                                          region_name=REGION,
                                          force_delete=True)
    
    print("LISTEN EM EXECUÇÃO")
    process_listener.listen()

listen = Thread(target=process)
listen.start()