FROM python:3.8.6-alpine

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["./gunicorn.sh"]