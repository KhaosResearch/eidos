from pathlib import Path
from typing import Any

import structlog

from eidos.models.function import load_model
from eidos.settings import settings
from eidos.utils import import_function, json_load
from eidos.validation.schema import validate_input_schema, validate_output_schema

log = structlog.get_logger("eidos.execution")


def get_openai_function_definition(name: str) -> dict[str, Any]:
    """
    Get the definition of a function and return it in a
    way that is compatible with OpenAI functions.

    Args:
        name (str): The name of the function.

    Returns:
        dict[str, Any]: The function definition in JSON Schema.
    """
    file_path = Path(settings.functions_folder) / f"{name}.json"
    function_definition = json_load(file_path)

    model = load_model(function_definition)
    parameters = model.model_json_schema()

    return {
        "name": function_definition["name"],
        "description": function_definition["description"],
        "parameters": parameters,
    }


def available_functions() -> list[dict[str, Any]]:
    """Get the list of available functions.

    Returns:
        list[dict[str, Any]]: The list of available functions.
    """
    return [
        json_load(file_path) for file_path in settings.functions_folder.glob("*.json")
    ]


def get_function_schema(function: str) -> dict[str, Any]:
    """Get the response schema of a function.

    Args:
        function (str): Name of the function.

    Returns:
        dict: Response schema of the function.
    """
    file_path = Path(settings.functions_folder) / f"{function}.json"
    function_definition = json_load(file_path)
    return function_definition["response"]


def list_functions_openai() -> list[dict[str, Any]]:
    """List all available AI functions.

    Returns:
        List of available AI functions.
    """
    return [get_openai_function_definition(fn["name"]) for fn in available_functions()]


def list_functions_names() -> list[str]:
    """List the names of all available AI functions.

    Returns:
        List of names of available AI functions.
    """
    return [fn["name"] for fn in available_functions()]


def execute(function_name: str, arguments: dict | None) -> dict[str, Any]:
    """
    Executes an AI function.

    Args:
        function_name: Name of the function to execute.
        arguments: Arguments to pass to the function.

    Returns:
        dict[str, Any]: The result of the function.
    """
    file_path = Path(settings.functions_folder) / f"{function_name}.json"

    try:
        function_definition = json_load(file_path)
    except FileNotFoundError:
        raise FileNotFoundError("Error: function module not found.")

    # Validate input arguments against the function's schema.
    if arguments:
        try:
            arguments = validate_input_schema(
                arguments, schema=function_definition["parameters"]
            )
        except (ValueError, TypeError) as e:
            log.error("Error: function arguments are malformed.", error=str(e))
            raise ValueError(f"Error: function arguments are malformed.\n{str(e)}")

    try:
        fn = import_function(function_definition["module"])
        result = fn(**arguments) if arguments else fn()
    except Exception as e:
        log.error("Error: function execution failed.", error=str(e))
        raise Exception(f"Error: function execution failed.\n{str(e)}")

    try:
        validated_result = validate_output_schema(
            result, schema=function_definition["response"].copy()
        )
    except (ValueError, TypeError) as e:
        log.error("Error: function result is malformed.", error=str(e))
        raise ValueError(f"Error: function result is malformed.\n{str(e)}")

    return validated_result
