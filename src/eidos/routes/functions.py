from fastapi import APIRouter, Security

from eidos.secure import get_api_key
from eidos.execution import (
    get_function_schema,
    get_openai_function_definition,
    list_functions_names,
    list_functions_openai,
)

router = APIRouter()


@router.get(
    "/",
    name="List available functions",
    tags=["functions"],
    response_model=list[dict],
)
async def list_functions_endpoint(api_key: str = Security(get_api_key)) -> list[dict]:
    """
    List all available AI functions.
    \f
    Args:
        api_key (str): API key.

    Returns:
        List of available AI functions.
    """
    return list_functions_openai()


@router.get(
    "/names",
    name="List the names of all available AI functions",
    tags=["functions"],
    response_model=list[str],
)
async def list_functions_names_endpoint(
    api_key: str = Security(get_api_key),
) -> list[str]:
    """
    List the names of all available AI functions.
    \f
    Args:
        api_key (str): API key.

    Returns:
        List of names of available AI functions.
    """
    return list_functions_names()


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

    return get_openai_function_definition(function)


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
    return get_function_schema(function)
