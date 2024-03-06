from typing import Any

from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse

from eidos.api.secure import get_api_key
from eidos.execution import execute

router = APIRouter()


@router.post(
    "/{function_name}",
    name="Execute an AI function",
    tags=["execution"],
    response_model=dict[str, Any],
)
async def execute_endpoint(
    function_name: str, arguments: dict, api_key: str = Security(get_api_key)
) -> dict[str, Any]:
    """
    Executes an AI function.
    \f
    Args:
        function_name: Name of the function to execute.
        arguments: Arguments to pass to the function.
        api_key: API key.

    Returns:
        Result of the function execution.
    """
    response, status = execute(function_name, arguments)
    return JSONResponse(response, status_code=status)
