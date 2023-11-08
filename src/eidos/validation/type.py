import builtins
from typing import Any

ALLOWED_TYPES = ["str", "int", "float", "bool", "list", "dict"]

ALLOWED_GENERIC_TYPES = ["str", "int", "float", "bool"]


def split_type_from_generic(type_: str) -> tuple[str, str | None]:
    """Remove the generic type from a type string.
    Args:
        type_ (str): Type string.
    Returns:
        str, str|None: Main type and generic type if it exists.
    """
    if "[" in type_ and "]" in type_:
        main_type, generic_type = type_.split("[")[0], type_.split("[")[1].rstrip("]")
    else:
        main_type, generic_type = type_, None
    return main_type, generic_type


def validate_type(value: Any, type_: str, allow_none: bool = False) -> bool:
    """Validate the type of a value.
    Args:
        value (Any): Value to validate.
        type (str): Type to validate the value against.
        allow_none (bool): Whether to allow None as a valid value.
    Returns:
        bool: True if the value is of the specified type, False otherwise.
    """
    if allow_none:
        if value is None:
            return True

    main_type, generic_type = split_type_from_generic(type_)
    if generic_type and main_type == "list":
        main_type_class = getattr(builtins, main_type)
        generic_type_class = getattr(builtins, generic_type)
        return isinstance(value, main_type_class) and all(
            isinstance(v, generic_type_class) for v in value
        )
    else:
        type_class = getattr(builtins, type_)

        return isinstance(value, type_class)


def get_type_as_string(x: Any) -> str:
    """Get the type of a variable as a string.

    Args:
        x (Any): Variable to get the type from.

    Returns:
        str: Type of the variable as a string.
    """
    return str(type(x)).split("'")[1]


def check_ai_parameter_types(values: dict) -> dict:
    """Check that the type is one of the allowed ones and
    that the options are of the correct type.
    Recursive types are not allowed. Dict generic types are not validated.
    """
    # Validate types
    type_ = values["type"]

    # Raises ValueError if the type is not valid
    validate_schema_type(type_)
    main_type, _ = split_type_from_generic(type_)

    # Regex and options are mutually exclusive
    if values["regex"] is not None and values["options"] is not None:
        raise ValueError("Regex and options are mutually exclusive")

    # Validate default value
    if not values["required"]:
        if values["default"] is not None:
            if get_type_as_string(values["default"]) != main_type:
                raise ValueError(
                    "Default value must be of the same type as the parameter"
                )

    # Validate regex
    if values["regex"] is not None:
        if main_type != "str":
            raise ValueError("Regex is only allowed for strings")

    # Validate options
    if values["options"] is not None:
        if len(values["options"]) == 0:
            raise ValueError("Options must be a non-empty list")
        if len(set(values["options"])) != len(values["options"]):
            raise ValueError("Options must be a list of unique values")

        for option in values["options"]:
            if not (main_type == get_type_as_string(option)):
                raise ValueError(
                    f"Options must be a list of {values['type']}, "
                    f"but {option} is {type(option)}"
                )
    return values


def validate_schema_type(schema_type: str) -> None:
    """Validate that the type of a parameter schema is allowed.
    This is used to check the parameters of an AI function is supported by eidos.
    Args:
        schema_type (str): Type of the schema.
    Raises:
        ValueError: If the type is not allowed.
    """
    main_type, generic_type = split_type_from_generic(schema_type)

    # Validate basic type
    if main_type not in ALLOWED_TYPES:
        raise ValueError(
            f"Type must be one of {ALLOWED_TYPES}. " f"Currently, it is {main_type}"
        )

    # If there is generic type, and the main type is a list
    if generic_type and main_type == "list":
        # Validate that the generic type is basic
        if generic_type not in ["str", "int", "float", "bool"]:
            raise ValueError(
                "Inner types are only allowed to be basic."
                f"Type must be one of {ALLOWED_GENERIC_TYPES}."
                f"Currently, it is {main_type}[{generic_type}]"
            )
