FROM python:3.10

# Install ASGI server
RUN pip install uvicorn

WORKDIR /code

COPY README.md /code/README.md
COPY ./src /code/src
COPY ./pyproject.toml /code/pyproject.toml
COPY ./functions /functions

ENV EIDOS_ENV production

ENV EIDOS_FUNCTIONS_FOLDER /functions

RUN pip install --no-cache-dir "."

EXPOSE 80

CMD ["uvicorn", "eidos.api:app", "--host", "0.0.0.0", "--port", "80"]
