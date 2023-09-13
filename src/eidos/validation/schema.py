from typing import Any

from eidos.validation.type import validate_type


def validate_output_schema(result: Any, schema: dict[str, Any]) -> dict[str, Any]:
    """Validate and transform the result of a function against its schema.
    Args:
        result (Any): Result of the function execution.
        schema (dict[str, Any]): Schema of the function response.
    Returns:
        dict[str, Any]: Validated and transformed result.
    """
    validated_result = {}
    if len(schema) == 1:
        out_variable, type_ = schema.popitem()
        if validate_type(result, type_):
            validated_result[out_variable] = result
        else:
            raise TypeError(f"Output variable {out_variable} is not of type {type_}.")
    else:
        for (out_variable, type_), result_value in zip(schema.items(), result):
            if validate_type(result_value, type_):
                validated_result[out_variable] = result_value
            else:
                raise TypeError(
                    f"Output variable {out_variable} is not of type {type_}."
                )

    return validated_result


def validate_input_schema(arguments: dict[str,], schema: list[dict[str, Any]]) -> None:
    """Validate the arguments of a function against its schema.
    Args:
        arguments (dict): Arguments to validate.
        schema (dict): Schema of the function arguments.
    Returns:
        None
    Raises:
        ValueError: If the number of arguments does not match the number of parameters.
        ValueError: If an argument is not found in the schema.
        TypeError: If an argument is not of the correct type.
    """
    types = [(parameter["name"], parameter["type"]) for parameter in schema]

    # Check that the number of arguments matches the number of parameters
    if len(arguments) != len(types):
        raise ValueError(
            f"Number of arguments ({len(arguments)}) does not match "
            f"number of parameters ({len(types)})"
        )

    # If they match, check that the arguments are of the correct type
    for schema_name, type_ in types:
        if schema_name not in arguments:
            raise ValueError(f"Argument {schema_name} not found in arguments")
        if not validate_type(arguments[schema_name], type_):
            raise TypeError(f"Argument {schema_name} is not of type {type_}")
