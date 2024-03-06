import structlog
from fastapi import APIRouter, Security

from eidos.execute import (
    get_function_schema,
    get_openai_function_definition,
    list_functions_names,
    list_functions_openai,
)
from eidos.secure import get_api_key

log = structlog.get_logger("eidos.functions")

router = APIRouter()


@router.get(
    "/",
    name="List available functions",
    tags=["functions"],
    response_model=list[dict],
)
async def list_functions_endpoint(_: str = Security(get_api_key)) -> list[dict]:
    """List all available functions."""
    return list_functions_openai()


@router.get(
    "/names",
    name="List the names of all available AI functions",
    tags=["functions"],
    response_model=list[str],
)
async def list_functions_names_endpoint(_: str = Security(get_api_key)) -> list[str]:
    """List function names."""
    return list_functions_names()


@router.get(
    "/{function}",
    name="Get definition of a function",
    tags=["functions"],
    response_model=dict,
)
async def function_definition(function: str, _: str = Security(get_api_key)) -> dict:
    """Get the definition of a function."""
    return get_openai_function_definition(function)


@router.get(
    "/{function}/schema",
    name="Get the response schema of a function",
    tags=["functions"],
    response_model=dict,
)
async def function_schema(function: str, _: str = Security(get_api_key)) -> dict:
    """Get the response schema of a function."""
    return get_function_schema(function)
