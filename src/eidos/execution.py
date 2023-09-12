import importlib
import json
from functools import lru_cache
from pathlib import Path

from eidos.logs import get_logger
from eidos.models.function import load_model
from eidos.settings import config

logger = get_logger()


@lru_cache
def get_local_function_definition(name: str) -> dict:
    file_ = Path(config.functions_folder / f"{name}.json")

    if not file_.exists():
        raise ValueError(f"Function not found: {name}")

    with open(file_, "r") as json_file:
        function_definition = json.load(json_file)

    return function_definition


def get_openai_function_definition(name: str) -> dict:
    """Get the definition of a function and return it in a
    way that is compatible with OpenAI functions.

    Args:
        name (str): The name of the function.

    Returns:
        dict: The function definition in JSON Schema.

    """
    function_definition = get_local_function_definition(name)

    AIFunction = load_model(function_definition)

    parameters = AIFunction.model_json_schema()

    return {
        "name": function_definition["name"],
        "description": function_definition["description"],
        "parameters": parameters,
    }


@lru_cache
def available_functions() -> list[dict[str, str]]:
    return [
        get_local_function_definition(file_.stem)
        for file_ in config.functions_folder.glob("*.json")
    ]


def import_function(module: str) -> callable:
    """Import a function from a module.

    Args:
        module (str): The module name, e.g., "pprint.pprint"

    Returns:
        callable: The function object
    """

    if "." not in module:
        raise ValueError("You can't import built-in modules")

    try:
        module_name, function_name = module.rsplit(".", 1)
        module = importlib.import_module(module_name)
        try:
            function_ = getattr(module, function_name)
            return function_
        except AttributeError as err:
            logger.error(
                f"Error: Function '{function_name}' "
                f"not found in module '{module_name}'."
            )
            raise err
    except (ValueError, ImportError) as err:
        logger.error(
            "Error: Unable to import module or "
            f"function from the provided name: '{module}'"
        )
        raise err
