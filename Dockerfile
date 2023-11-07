FROM python:3.10-slim-buster

WORKDIR /code

COPY pyproject.toml .
COPY README.md .
COPY src/ ./src/
COPY functions/ ./functions/

RUN pip install "."

ENTRYPOINT [ "python", "-m", "eidos" ]

EXPOSE 6004

CMD [ "server" ]