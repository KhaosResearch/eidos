from enum import Enum
from typing import Any

import structlog

from eidos.execute import (
    execute,
    get_function_schema,
    get_openai_function_definition,
    list_functions_names,
    list_functions_openai,
)

log = structlog.get_logger("eidos.lambda")


class ValidationCommands(Enum):
    """Enum to hold the different validation commands from eidos."""

    LIST = "LIST"
    LIST_NAMES = "LIST_NAMES"
    GET_DEFINITION = "GET_DEFINITION"
    GET_SCHEMA = "GET_SCHEMA"
    EXECUTE = "EXECUTE"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


def lambda_handler(event: dict[str, Any], context: dict[str, Any]):
    try:
        log.info("Processing event", command=event["command"])
        command = event["command"]
    except KeyError:
        raise ValueError(
            f"There is a required field 'command' with the function to execute. "
            f"Possible values: {ValidationCommands.__members__}"
        )

    try:
        validation_function = ValidationCommands[command]
    except KeyError:
        raise ValueError(
            f"Unknown function: {event['command']}. "
            f"Possible values: {ValidationCommands.__members__}"
        )

    match validation_function:
        case ValidationCommands.LIST:
            return list_functions_openai()
        case ValidationCommands.LIST_NAMES:
            return list_functions_names()
        case ValidationCommands.GET_DEFINITION:
            if "function" in event.get("parameters", {}):
                function = event["parameters"]["function"]
                return get_openai_function_definition(function)
            else:
                return {
                    "statusCode": 400,
                    "body": "Missing function. Provide as parameters.function",
                }
        case ValidationCommands.GET_SCHEMA:
            if "function" in event.get("parameters", {}):
                function = event["parameters"]["function"]
                return get_function_schema(function)
            else:
                return {
                    "statusCode": 400,
                    "body": "Missing function. Provide as parameters.function",
                }
        case ValidationCommands.EXECUTE:
            if "function" in event.get("parameters", {}):
                function = event["parameters"]["function"]
            else:
                return {
                    "statusCode": 400,
                    "body": "Missing function. Provide as parameters.function",
                }

            args = event["parameters"].get("args", {})  # Default to empty parameters
            log.info("Executing function ", function=function, arguments=args)

            result = execute(function, args)

            return result
        case _:
            raise ValueError(
                f"Unknown function: {event['command']}. "
                f"Possible values: {ValidationCommands.__members__}"
            )
