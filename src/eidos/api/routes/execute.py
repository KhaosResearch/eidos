from fastapi import APIRouter

from eidos.execution import get_local_function_definition, import_function
from eidos.logs import get_logger

logger = get_logger("eidos.api.execute")

router = APIRouter()


@router.post(
    "/{function_name}",
    name="Execute an AI function",
    tags=["execution"],
    response_model=str,
)
async def execute(function_name: str, arguments: dict) -> str:
    """
    Executes an AI function.

    Args:
        function_name: Name of the function to execute.
        arguments: Arguments to pass to the function.

    Returns:
        Result of the function execution.
    """
    function_definition = get_local_function_definition(function_name)

    result = import_function(function_definition["module"])(**arguments)

    return str(result)
