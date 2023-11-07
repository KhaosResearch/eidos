import importlib

from eidos.logs import get_logger

logger = get_logger()


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
