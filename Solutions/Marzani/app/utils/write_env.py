import os

# Arquivo para pegar as variáveis de ambiente do .env e as utilizar nos arquivos necessários para reduzir código
# e possíveis problemas em sobrescrever.

# Pegando as variáveis de ambiente e colocando o parâmetro adicional caso ele não encontre.

URL = os.getenv('URL', 'http://host.docker.internal:4566/health')
SQS_IN = os.getenv('SQS_IN', 'http://host.docker.internal:4566/000000000000/InputQueue.fifo')
SQS_IN_NAME = os.getenv('SQS_IN_NAME', 'InputQueue')
SQS_OUT_NAME = os.getenv('SQS_OUT_NAME', 'OutputQueue')
SQS_OUT = os.getenv('SQS_OUT', 'http://host.docker.internal:4566/000000000000/OutputQueue.fifo')
ENDPOINT_URL = os.getenv('ENDPOINT_URL', 'http://host.docker.internal:4566/')
KEY_ID = os.getenv('KEY_ID', 'test')
ACCESS_KEY = os.getenv('ACCESS_KEY', 'test')
REGION = os.getenv('REGION', 'us-east-1')
