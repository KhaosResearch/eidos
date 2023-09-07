from fastapi import APIRouter

from eidos.logs import get_logger

logger = get_logger("eidos.api.functions")

router = APIRouter()


@router.get(
    "/",
    name="List available functions",
    tags=["functions"],
    response_model=list[str],
)
async def list() -> str:
    """
    List all available AI functions.

    Args:
        None

    Returns:
        List of available AI functions.
    """

    return ["hello_world"]
