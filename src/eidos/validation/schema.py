from typing import Any

from eidos.validation.type import is_value_of_type


def validate_input_schema(
    input_arguments: dict[str, Any], schema: list[dict[str, Any]]
) -> dict[str, Any]:
    """Validates input arguments against a predefined schema.

    Args:
        input_arguments (dict): Arguments to validate.
        schema (dict): Schema of the function arguments.

    Returns:
        dict[str, Any]: Validated and transformed arguments.
    """
    schema_keys = {param["name"] for param in schema}

    # Check for unknown arguments.
    for arg_key in input_arguments.keys():
        if arg_key not in schema_keys:
            raise ValueError(f"Unknown argument {arg_key}: not found in schema.")

    validated_arguments = {}
    for param in schema:
        param_name = param["name"]
        is_required = param.get("required", True)
        param_type = param["type"]
        param_default = param.get("default", None)

        if param_name not in input_arguments:
            if is_required:
                raise ValueError(
                    f"Argument {param_name} is required but was not provided."
                )
            else:
                validated_arguments[param_name] = param_default
        else:
            arg_value = input_arguments[param_name]
            if not is_value_of_type(
                arg_value, param_type, accept_none=param_default is None
            ):
                raise TypeError(
                    f"Argument {param_name} is not of type {param_type}. Got {type(arg_value).__name__} instead."
                )
            validated_arguments[param_name] = arg_value

    return validated_arguments


def validate_output_schema(output: Any, schema: dict[str, Any]) -> dict[str, Any]:
    """Validates and formats the output of a function based on a predefined schema.

    Args:
        output (Any): The output of the function to validate and format.
        schema (dict[str, Any]): A schema defining the expected structure and types of the function output.
            Each key in the schema represents an output variable name, and the associated
            value specifies the expected type of that output variable.

    Returns:
        dict[str, Any]: Validated and transformed result.
    """
    formatted_output = {}
    if len(schema) == 1:
        variable_name, expected_type = schema.popitem()
        if is_value_of_type(output, expected_type):
            formatted_output[variable_name] = output
        else:
            raise TypeError(
                f"Output variable {variable_name} is not of the expected type {expected_type}."
            )
    else:
        len_result = 1 if isinstance(output, str) else len(output)

        if len_result != len(schema):
            raise ValueError(
                f"Number of output variables ({len_result}) does not match "
                f"number of variables in the schema ({len(schema)})"
            )
        for (out_variable, type_), result_value in zip(schema.items(), output):
            if is_value_of_type(result_value, type_, accept_none=True):
                formatted_output[out_variable] = result_value
            else:
                raise TypeError(
                    f"Output variable {out_variable} is not of type {type_}."
                )

    return formatted_output
