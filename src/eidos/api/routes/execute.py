from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from eidos.execution import get_eidos_function_definition, import_function
from eidos.logs import get_logger

logger = get_logger("eidos.api.execute")

router = APIRouter()


@router.post(
    "/{function_name}",
    name="Execute an AI function",
    tags=["execution"],
    response_model=dict[str, Any],
)
async def execute(function_name: str, arguments: dict) -> dict[str, Any]:
    """
    Executes an AI function.

    Args:
        function_name: Name of the function to execute.
        arguments: Arguments to pass to the function.

    Returns:
        Result of the function execution.
    """
    function_definition = get_eidos_function_definition(function_name)

    error = None
    try:
        result = import_function(function_definition["module"])(**arguments)
    except Exception as e:
        logger.error(f"Error executing function {function_name}: {e}")
        error = str(e)

    if error is None:
        status = 200
        response = {
            "status": {
                "code": status,
                "message": "Success",
            },
            "data": result,
        }
    else:
        status = 500
        response = {
            "status": {
                "code": status,
                "message": f"Error: function execution failed.\n{error}",
            },
            "data": None,
        }

    return JSONResponse(response, status_code=status)
