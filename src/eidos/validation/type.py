import builtins
from typing import Any

ALLOWED_TYPES = ["str", "int", "float", "bool", "list", "dict"]

ALLOWED_GENERIC_TYPES = ["str", "int", "float", "bool"]


def parse_type_name(type_str: str) -> tuple[str, str | None]:
    """Extracts the base type and the generic (contained) type from a type string.

    This function parses a type string that may include generic type information enclosed in brackets.

    Args:
        type_str (str): Type string.

    Returns:
        tuple[str, str | None]: A tuple containing the base type as the first element and the generic
        type as the second element (None if not applicable).
    """
    if not type_str:
        raise ValueError("Empty type string.")
    if type_str.count("[") != type_str.count("]"):
        raise ValueError("Unmatched brackets in type string.")

    if "[" in type_str and "]" in type_str:
        # Find the first occurrence of '[' to avoid splitting nested generics
        split_index = type_str.find("[")
        if split_index == 0:
            raise ValueError("Invalid type string.")
        base_type = type_str[:split_index]
        # Extract generic type, considering nested generics by finding the last ']'
        contained_type = type_str[split_index + 1 : type_str.rfind("]")]
    else:
        base_type, contained_type = type_str, None

    return base_type, contained_type


def is_value_of_type(value: Any, type_str: str, accept_none: bool = False) -> bool:
    """Checks if the provided value matches the expected type, optionally allowing None.

    Args:
        value (Any): Value to validate.
        type_str (str): Type to validate the value against.
        accept_none (bool): Whether to allow None as a valid value.

    Returns:
        bool: True if the value is of the specified type, False otherwise.
    """
    if accept_none and value is None:
        return True

    main_type, contained_type = parse_type_name(type_str)

    if main_type == "list" and contained_type is not None:
        contained_type_class = getattr(builtins, contained_type)
        # Validate each element in the list if it matches the contained type.
        if accept_none:
            all_elements_match_type = all(
                (isinstance(element, contained_type_class) or element is None)
                for element in value
            )
        else:
            all_elements_match_type = all(
                isinstance(element, contained_type_class) for element in value
            )
        return all_elements_match_type
    else:
        type_class = getattr(builtins, type_str)
        return isinstance(value, type_class)


def get_variable_type_name(variable: Any) -> str:
    """Retrieves the name of the type of the provided variable as a string.

    Args:
        variable (Any): Variable to get the type from.

    Returns:
        str: Type of the variable as a string.
    """
    return type(variable).__name__


def validate_schema_type(schema_type: str) -> None:
    """
    Validates the schema type of a parameter.

    Args:
        schema_type (str): Type of the schema.

    Raises:
        ValueError: If the type is not allowed.
    """
    main_type, generic_type = parse_type_name(schema_type)

    if main_type not in ALLOWED_TYPES:
        allowed_types_str = ", ".join(ALLOWED_TYPES)
        raise ValueError(
            f"Type '{main_type}' is not allowed. Allowed types are: {allowed_types_str}."
        )

    if generic_type and main_type == "list":
        if generic_type not in ALLOWED_GENERIC_TYPES:
            allowed_generic_types_str = ", ".join(ALLOWED_GENERIC_TYPES)
            raise ValueError(
                f"Generic type '{generic_type}' is not allowed for 'list'. Allowed generic types are: {allowed_generic_types_str}. Currently, it is '{main_type}[{generic_type}]'."
            )
