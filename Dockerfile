FROM python:3.10-slim-buster

WORKDIR /code

COPY pyproject.toml .
COPY README.md .
COPY src/ .
COPY functions/ .

RUN pip install ".[ai]"

ENTRYPOINT [ "python", "-m", "eidos" ]

CMD [ "server" ]