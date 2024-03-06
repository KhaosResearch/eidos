FROM python:3.10

WORKDIR /code

COPY README.md /code/README.md
COPY ./src /code/src
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install "."

EXPOSE 80

CMD ["uvicorn", "src.eidos.main:app", "--host", "0.0.0.0", "--port", "80"]