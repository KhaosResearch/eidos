from typing import Any

import structlog
from eidos.execute import execute
from eidos.secure import query_scheme
from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse

log = structlog.get_logger("eidos.execution")

router = APIRouter()


@router.post(
    "/{function_name}",
    name="Execute an AI function",
    tags=["execution"],
    response_model=dict[str, Any],
)
async def execute_endpoint(
    function_name: str, arguments: dict | None = None, _: str = Security(query_scheme)
) -> JSONResponse:
    """Executes an AI function with the given arguments."""
    try:
        data = execute(function_name, arguments)
        response, status = (
            {
                "status": {
                    "code": 200,
                    "message": "Success",
                },
                "data": data,
            },
            200,
        )
    except Exception as e:
        response, status = (
            {
                "status": {
                    "code": 500,
                    "message": str(e),
                },
                "data": None,
            },
            500,
        )
    return JSONResponse(content=response, status_code=status)
