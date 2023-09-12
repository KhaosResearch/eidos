from fastapi import APIRouter

from eidos.execution import available_functions, get_openai_function_definition
from eidos.logs import get_logger

logger = get_logger("eidos.api.functions")

router = APIRouter()


@router.get(
    "/",
    name="List available functions",
    tags=["functions"],
    response_model=list[dict],
)
async def list_functions() -> list[dict]:
    """
    List all available AI functions.

    Args:
        None

    Returns:
        List of available AI functions.
    """

    return available_functions()


@router.get(
    "/names",
    name="List the names of all available AI functions",
    tags=["functions"],
    response_model=list[str],
)
async def list_functions_names() -> list[str]:
    """
    List the names of all available AI functions.

    Args:
        None

    Returns:
        List of names of available AI functions.
    """
    return [function_["name"] for function_ in available_functions()]


@router.get(
    "/{function}",
    name="Get definition of a function",
    tags=["functions"],
    response_model=dict,
)
async def function_definition(function: str) -> dict:
    """Get the definition of a function.

    Args:
        function (str): Name of the function.

    Returns:
        dict: Definition of the function.
    """
    function_json = get_openai_function_definition(function)

    return function_json
