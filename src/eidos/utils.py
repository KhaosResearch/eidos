import importlib
import json
from functools import lru_cache
from pathlib import Path

import structlog

log = structlog.get_logger("eidos.utils")


@lru_cache(maxsize=128)
def json_load(file_path: str | Path) -> dict:
    """Loads a JSON file.

    Args:
        file_path (str): The file path.

    Returns:
        dict: The JSON file as a dictionary.
    """
    with open(file_path, "r") as json_file:
        return json.load(json_file)


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
            log.error(
                "Error: Function not found in module",
                module_name=module_name,
                function_name=function_name,
            )
            raise err
    except (ValueError, ImportError) as err:
        log.error("Error: Failed to import function", module_name=module)
        raise err
