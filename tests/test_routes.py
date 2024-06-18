from eidos.api import app
from eidos.secure import query_scheme
from fastapi.testclient import TestClient

client = TestClient(
    app,
    # Remove the root path (if any).
    root_path="",
)


async def override_query_scheme():
    return


app.dependency_overrides[query_scheme] = override_query_scheme


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_function_definition():
    response = client.get("/api/v1/functions/salute")
    assert response.status_code == 200
    assert response.json() == {
        "description": "Say hello to someone.",
        "name": "salute",
        "parameters": {
            "properties": {
                "who": {
                    "description": "Name of whom to salute. o7",
                    "title": "Who",
                    "type": "string",
                }
            },
            "required": ["who"],
            "title": "salute",
            "type": "object",
        },
    }


def test_function_schema():
    response = client.get("/api/v1/functions/salute/schema")
    assert response.status_code == 200
    assert response.json() == {"msg": "str"}


def test_function_execute():
    response = client.post("/api/v1/execution/salute", json={"who": "Nikos"})
    assert response.status_code == 200
    assert response.json() == {
        "data": {"msg": "Hello, Nikos! o7"},
        "status": {"code": 200, "message": "Success"},
    }


def test_function_execute_with_no_arguments():
    response = client.post("/api/v1/execution/salute")
    assert response.status_code == 500
    assert response.json() == {
        "data": None,
        "status": {
            "code": 500,
            "message": "Error: function execution failed.\nsalute() missing 1 required positional argument: 'who'",
        },
    }


def test_function_execute_missing():
    response = client.post("/api/v1/execution/nonexistent", json={})
    assert response.status_code == 500
    assert response.json() == {
        "data": None,
        "status": {"code": 500, "message": "Error: function module not found."},
    }


def test_function_execute_bad_arguments():
    response = client.post("/api/v1/execution/salute", json={"hey": "Nikos"})
    assert response.status_code == 500
    assert response.json() == {
        "data": None,
        "status": {
            "code": 500,
            "message": "Error: function arguments are malformed.\nUnknown argument hey: not found in schema.",
        },
    }
