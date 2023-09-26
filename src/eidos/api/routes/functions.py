from fastapi import APIRouter, Security

from eidos.api.secure import get_api_key
from eidos.execution import (
    available_functions,
    get_eidos_function_definition,
    get_openai_function_definition,
)
from eidos.logs import get_logger

logger = get_logger("eidos.api.functions")

router = APIRouter()


@router.get(
    "/",
    name="List available functions",
    tags=["functions"],
    response_model=list[dict],
)
async def list_functions(api_key: str = Security(get_api_key)) -> list[dict]:
    """
    List all available AI functions.
    \f
    Args:
        api_key (str): API key.

    Returns:
        List of available AI functions.
    """
    return [
        get_openai_function_definition(function_["name"])
        for function_ in available_functions()
    ]


@router.get(
    "/names",
    name="List the names of all available AI functions",
    tags=["functions"],
    response_model=list[str],
)
async def list_functions_names(api_key: str = Security(get_api_key)) -> list[str]:
    """
    List the names of all available AI functions.
    \f
    Args:
        api_key (str): API key.

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
async def function_definition(
    function: str, api_key: str = Security(get_api_key)
) -> dict:
    """Get the definition of a function.
    \f
    Args:
        function (str): Name of the function.
        api_key (str): API key.

    Returns:
        dict: Definition of the function.
    """
    function_json = get_openai_function_definition(function)

    return function_json


@router.get(
    "/{function}/schema",
    name="Get the response schema of a function",
    tags=["functions"],
    response_model=dict,
)
async def function_schema(function: str, api_key: str = Security(get_api_key)) -> dict:
    """Get the response schema of a function.
    \f
    Args:
        function (str): Name of the function.
        api_key (str): API key.

    Returns:
        dict: Response schema of the function.
    """
    function_json = get_eidos_function_definition(function)

    return function_json["response"]
