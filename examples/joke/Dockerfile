FROM eidos:latest

WORKDIR /app

COPY app /app/joke
COPY setup.py /app/setup.py
COPY joke.json /functions/joke.json

RUN pip install "."