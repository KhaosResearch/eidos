from typing import Any

from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse

from eidos.api.secure import get_api_key
from eidos.execution import get_eidos_function_definition, import_function
from eidos.logs import get_logger
from eidos.validation.schema import validate_input_schema, validate_output_schema

logger = get_logger("eidos.api.execute")

router = APIRouter()


@router.post(
    "/{function_name}",
    name="Execute an AI function",
    tags=["execution"],
    response_model=dict[str, Any],
)
async def execute(
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
    function_definition = get_eidos_function_definition(function_name)

    # Validate inputs
    try:
        validate_input_schema(arguments, schema=function_definition["parameters"])
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid input: {e}")
        status = 400
        response = {
            "status": {
                "code": status,
                "message": f"Error: malformed function call.\n{str(e)}",
            },
            "data": None,
        }

        return JSONResponse(response, status_code=status)

    # Execute function
    try:
        result = import_function(function_definition["module"])(**arguments)
    except Exception as e:
        logger.error(f"Error executing function {function_name}: {e}")
        status = 500
        response = {
            "status": {
                "code": status,
                "message": f"Error: function execution failed.\n{str(e)}",
            },
            "data": None,
        }

        return JSONResponse(response, status_code=status)

    # Validate and transform result
    try:
        validated_result = validate_output_schema(
            result, schema=function_definition["response"].copy()
        )
    except (ValueError, TypeError) as e:
        status = 500
        response = {
            "status": {
                "code": status,
                "message": f"Error: function return malformed results.\n{str(e)}",
            },
            "data": None,
        }

        return JSONResponse(response, status_code=status)

    # Return validated results
    status = 200
    response = {
        "status": {
            "code": status,
            "message": "Success",
        },
        "data": validated_result,
    }

    return JSONResponse(response, status_code=status)
