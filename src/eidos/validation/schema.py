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
            if validate_type(result_value, type_, allow_none=True):
                validated_result[out_variable] = result_value
            else:
                raise TypeError(
                    f"Output variable {out_variable} is not of type {type_}."
                )

    return validated_result


def validate_input_schema(
    arguments: dict[str, Any], schema: list[dict[str, Any]]
) -> dict[str, Any]:
    """Validate and add any optional arguments of a function against its schema.
    Args:
        arguments (dict): Arguments to validate.
        schema (dict): Schema of the function arguments.
    Returns:
        dict[str, Any]: Validated and transformed arguments.
    Raises:
        ValueError: If there is a missing argument
        ValueError: If an argument is not found in the schema.
        TypeError: If an argument is not of the correct type.
    """
    schema_names = [parameter["name"] for parameter in schema]

    for key in arguments:
        if key not in schema_names:
            raise ValueError(f"Unknown agument {key}: not found in schema")

    # If they match, check that the arguments are of the correct type
    for parameter in schema:
        required = parameter["required"]
        schema_name = parameter["name"]
        type_ = parameter["type"]

        if required is None or required:  # If required is None, it is defined as True
            if schema_name not in arguments:
                raise ValueError(f"Argument {schema_name} not found in arguments")

            if not validate_type(arguments[schema_name], type_, allow_none=False):
                raise TypeError(
                    f"Argument {schema_name} is not of type {type_}. "
                    f"Got {type(arguments[schema_name])} instead."
                )
        else:  # If required is False, add the default value
            if schema_name not in arguments:
                arguments[schema_name] = parameter["default"]
            # None must be a valid type if it's marked as default.
            if not validate_type(arguments[schema_name], type_, allow_none=True):
                raise TypeError(
                    f"Argument {schema_name} is not of type {type_}. "
                    f"Got {type(arguments[schema_name])} instead."
                )
    return arguments
