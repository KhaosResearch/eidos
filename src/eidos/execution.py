import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from eidos.logs import get_logger
from eidos.models.function import load_model
from eidos.settings import config
from eidos.utils import import_function
from eidos.validation.schema import validate_input_schema, validate_output_schema

logger = get_logger()


@lru_cache
def get_eidos_function_definition(name: str) -> dict[str, Any]:
    """Get the definition of a function in the eidos format.

    Args:
        name (str): The name of the function.

    Returns:
        dict[str, Any]: The function definition in internal format.
    """
    file_ = Path(config.functions_folder / f"{name}.json")

    if not file_.exists():
        logger.error(f"Function not found: {name}")
        raise ValueError(f"Function not found: {name}")

    with open(file_, "r") as json_file:
        function_definition = json.load(json_file)

    return function_definition


def get_openai_function_definition(name: str) -> dict[str, Any]:
    """Get the definition of a function and return it in a
    way that is compatible with OpenAI functions.

    Args:
        name (str): The name of the function.

    Returns:
        dict[str, Any]: The function definition in JSON Schema.
    """
    function_definition = get_eidos_function_definition(name)

    AIFunction = load_model(function_definition)

    parameters = AIFunction.model_json_schema()

    return {
        "name": function_definition["name"],
        "description": function_definition["description"],
        "parameters": parameters,
    }


@lru_cache
def available_functions() -> list[dict[str, Any]]:
    """Get the list of available functions.

    Returns:
        list[dict[str, str]]: The list of available functions.
    """
    return [
        get_eidos_function_definition(file_.stem)
        for file_ in config.functions_folder.glob("*.json")
    ]


def get_function_schema(function: str) -> dict[str, Any]:
    """Get the response schema of a function.

    Args:
        function (str): Name of the function.

    Returns:
        dict: Response schema of the function.
    """
    function_json = get_eidos_function_definition(function)

    return function_json["response"]


def list_functions_openai() -> list[dict[str, Any]]:
    """List all available AI functions.

    Returns:
        List of available AI functions.
    """
    return [
        get_openai_function_definition(function_["name"])
        for function_ in available_functions()
    ]


def list_functions_names() -> list[str]:
    """List the names of all available AI functions.

    Returns:
        List of names of available AI functions.
    """
    return [function_["name"] for function_ in available_functions()]


def execute(function_name: str, arguments: dict) -> tuple[dict[str, Any], int]:
    """
    Executes an AI function.

    Args:
        function_name: Name of the function to execute.
        arguments: Arguments to pass to the function.

    Returns:
        tuple[dict[str, Any], int]: Result of the function execution and a status code.
    """
    function_definition = get_eidos_function_definition(function_name)

    # Validate inputs
    try:
        arguments = validate_input_schema(
            arguments, schema=function_definition["parameters"]
        )
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid input: {e}")
        status = 400
        response = {
            "status": {
                "code": status,
                "message": f"Error: malformed function call.\n{str(e)}",
            },
            "data": None,
        }

        return response, status

    # Execute function
    try:
        result = import_function(function_definition["module"])(**arguments)
    except Exception as e:
        logger.error(f"Error executing function {function_name}: {e}")
        status = 500
        response = {
            "status": {
                "code": status,
                "message": f"Error: function execution failed.\n{str(e)}",
            },
            "data": None,
        }

        return response, status

    # Validate and transform result
    try:
        validated_result = validate_output_schema(
            result, schema=function_definition["response"].copy()
        )
    except (ValueError, TypeError) as e:
        status = 500
        response = {
            "status": {
                "code": status,
                "message": f"Error: function return malformed results.\n{str(e)}",
            },
            "data": None,
        }

        return response, status

    # Return validated results
    status = 200
    response = {
        "status": {
            "code": status,
            "message": "Success",
        },
        "data": validated_result,
    }

    return response, status
