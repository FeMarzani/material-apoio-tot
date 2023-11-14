# Desenvolvimento de uma API que suporta longas durações de processamento


### Ferramentas utilizadas:
<div align="center">
  <img align="center" alt="Python" height="30" src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" />
  <img align="center" alt="Git" height="28" width="42" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg">
  <img align="center" alt="AWS" height="28" width="42" src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1024px-Amazon_Web_Services_Logo.svg.png" />
  <img align="center" alt="localstack" height="28" width="42" src="https://avatars.githubusercontent.com/u/28732122?s=200&v=4"/>
  <img align="center" alt="Marzani-Flask" height="28" width="42" src="https://raw.githubusercontent.com/devicons/devicon/v2.15.1/icons/flask/flask-original-wordmark.svg">
  <img align="center" alt="Marzani-Docker" height="28" width="42" src="https://icongr.am/devicon/docker-original.svg?size=148&color=00f030" />
  <img align="center" alt="Gunicorn" height="28" width="42" src="https://gunicorn.org/images/logo.jpg" />
  - PySQSListener
</div>

### Descrição:
- API Flask, com duas rotas não bloqueantes:    

    - Rota `/health` para checar o healthcheck do container, que deve retornar o código http correto, conforme normas para uma API REST. Nesta API, a rota `/health` está retornando a healthcheck do localstack através de uma requisição GET. Ao realizar o GET nesta rota, o retorno terá a seguinte representação como base:

        ```json
        {
        "body": {
            "edition": "community",
            "services": {
            "acm": "available",
            ...
            },
            "version": "2.3.3.dev"
        },
        "statusCode": 200
        }
        ```

    - Rota `/` para realizar o pooling de mensagens na fila de entrada. Para isso, utilizou-se:

        - 2 Buckets do S3:
            - Um para salvar arquivos de Scifi;

            - Um para salvar arquivos de Romance.
            
        - 2 Filas SQS do tipo FIFO:
            - InputQueue - Para receber as mensagens que serão desserializadas para posterior upload nos respectivos buckets.

            - OutpuQueue - Irá ser utilizada para disparo de uma mensagem após o sucesso de realização do upload do JSON, possuindo dados de nome do arquivo e bucket.

Ao receber uma nova mensagem, a mesma será processada continuamente, ou seja, será desserealizada a mensagem recebida em um dicionário para consumir os valores. Para manter o processo monitorando a fila, utilizou-se o PySQSListener.

A mensagem irá conter:

```json
    {
     "id": "12345",
     "title": "LoremIpsum",
     "author": "John Doe",
     "year": "1960",
     "genre": "romance",
     "summary": "Lorem ipsum dolor sit amet, 
                 consectetur adipiscing elit,
                 sed do eiusmod tempor incididunt
                 ut labore et dolore magna aliqua."
    }
```

Sendo que:
- `title`: nome doo arquivo a ser salvo no bucket.
- `genre`: define qual bucket o arquivo será salvo. 

O arquivo consiste da própria mensagem, em formato json e será salvo, com extensão no bucket referente ao gênero do mesmo.

### Como instalar e rodar a aplicação:
Baixe os arquivos do repositório pelo zip, ou clone o repositório.

```bash
git clone https://github.com/FeMarzani/material-apoio-tot.git
```

Navegue até a pasta de app, dentro do exercicio01_marzani que está na pasta de Solutions.
```bash
cd Solutions
cd exercicio01_marzani
cd app
```

Deseja setar as variáveis de ambiente? Para rodar a aplicação no docker utilizando localstack, use as variáveis do modelo abaixo:

```
URL=http://host.docker.internal:4566/health
SQS_IN=http://host.docker.internal:4566/000000000000/InputQueue.fifo
SQS_IN_NAME=InputQueue
SQS_OUT_NAME=OutputQueue
SQS_OUT=http://host.docker.internal:4566/000000000000/OutputQueue.fifo
ENDPOINT_URL=http://host.docker.internal:4566/
KEY_ID=test
ACCESS_KEY=test
REGION=us-east-1
```

Se desejar testar utilizando o localstack, tenha-o em execução e crie as seguintes filas e buckets:

```sh
#!/bin/sh

# Create the buckets
echo "Creating buckets ..."
awslocal s3api create-bucket --bucket scifi
awslocal s3api create-bucket --bucket romance

# Create the queues using awslocal
echo "Creating the queues ..."
awslocal sqs create-queue --queue-name InputQueue.fifo --attributes FifoQueue=true
awslocal sqs create-queue --queue-name OutputQueue.fifo --attributes FifoQueue=true
```

Agora build a imagem do docker e depois execute.

```bash
docker build -t app .
```

```bash
docker run -p 5000:5000 -d app
```

A partir disso sua aplicação estará em funcionamento. Para testar se a mensagem será desserializada após o upload desta na fila SQS, envie uma mensagem a partir do modelo abaixo:

```sh
#!/bin/sh

# Sends a message to the pdf-new queue
echo "Sending a message to the InputQueue..."

awslocal sqs send-message --queue-url http://localhost:4566/000000000000/InputQueue.fifo --message-group-id "test" --message-deduplication-id "test" --message-body '{"id": "1452345", "title":"Testando", "author": "John Doe", "year":"1960", "genre":"scifi", "summary":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}'
```