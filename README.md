# eidos:  Validation and execution of AI functions

_eidos_ is an API for validating and executing AI functions. It aims to be a generic API to serve as a common interface to allow execution of functions by LLMs.

![Usage diagram of eidos](assets/eidos.png)

## Install

From source:

```bash
git clone git@github.com:KhaosResearch/eidos.git
cd eidos
python -m pip install -e .
```

Or directly from GitHub:

```bash
python -m pip install "eidos @ git+ssh://git@github.com/KhaosResearch/eidos.git"
```

## Run

Run the API with the following command:

```bash
uvicorn eidos.api:app --host 0.0.0.0 --port 8090 --reload
```

You can override the default configuration by setting [environment variables](src/eidos/settings.py).

Alternatively, you can use the provided [Dockerfile](Dockerfile) to build a Docker image and run the API in a container:

```bash
docker build -t eidos-server:latest .
docker run -v $(pwd)/functions:/functions -p 8090:80 eidos-server:latest
```

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"who": "me"}' http://localhost:8090/api/v1/execution/salute
```

To deploy the container in Kubernetes, a reference deployment is available and documented at [deployments](deployments/).

## Testing

`pytest` is used for testing. You can run the tests with the following command:

```bash
pytest tests/
```
