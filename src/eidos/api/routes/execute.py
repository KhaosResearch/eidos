from fastapi import APIRouter

from eidos.logs import get_logger

logger = get_logger("eidos.api.execute")

router = APIRouter()


@router.get(
    "/{function_}",
    name="Execute an AI function",
    tags=["execution"],
    response_model=str,
)
async def execute(function_: str) -> str:
    """
    Executes an AI function.

    Args:
        function_: Name of the function to execute.

    Returns:
        Result of the function execution.
    """

    return function_
