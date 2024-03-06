import pytest
from eidos.validation.type import (
    get_variable_type_name,
    is_value_of_type,
    parse_type_name,
    validate_schema_type,
)


@pytest.mark.parametrize(
    "type_str, expected",
    [
        ("int", ("int", None)),  # Simple type without generic
        ("List[int]", ("List", "int")),  # Single generic
        ("Dict[str, int]", ("Dict", "str, int")),  # Generic with comma
        (
            "List[Dict[str, List[int]]]",
            ("List", "Dict[str, List[int]]"),
        ),  # Nested generics
        (
            "CustomType[AnotherType]",
            ("CustomType", "AnotherType"),
        ),  # Custom types with generics
    ],
)
def test_parse_type_name(type_str, expected):
    assert parse_type_name(type_str) == expected


@pytest.mark.parametrize(
    "invalid_type_str",
    [
        "",  # Empty string
        "[]",  # Only brackets
        "Type[",  # Missing closing bracket
        "Type]",  # Missing opening bracket
    ],
)
def test_parse_type_name_with_invalid_input(invalid_type_str):
    with pytest.raises(ValueError):
        parse_type_name(invalid_type_str)


@pytest.mark.parametrize(
    "value,type_str,accept_none,expected_result",
    [
        (123, "int", False, True),
        ("test", "str", False, True),
        ([1, 2, 3], "list[int]", False, True),
        ([1, "2", 3], "list[int]", False, False),
        (None, "str", True, True),
        ({"key": "value"}, "dict", False, True),
        (None, "dict", False, False),
    ],
)
def test_is_value_of_type(value, type_str, accept_none, expected_result):
    assert is_value_of_type(value, type_str, accept_none) == expected_result


@pytest.mark.parametrize(
    "variable,type_str",
    [
        (123, "int"),
        ("test", "str"),
        ([1, 2, 3], "list"),
        ({"key": "value"}, "dict"),
        (None, "NoneType"),
        (True, "bool"),
    ],
)
def test_get_variable_type_name(variable, type_str):
    assert get_variable_type_name(variable) == type_str


@pytest.mark.parametrize(
    "schema_type",
    [
        "str",
        "int",
        "float",
        "bool",
        "list[str]",
        "list[int]",
        "list[float]",
        "list[bool]",
    ],
)
def test_validate_schema_type_success(schema_type):
    validate_schema_type(schema_type)


@pytest.mark.parametrize(
    "schema_type",
    [
        "set",
        "tuple",
    ],
)
def test_validate_schema_type_main_type_failure(schema_type):
    with pytest.raises(ValueError) as exc_info:
        validate_schema_type(schema_type)
    assert "Type" in str(exc_info.value) and "is not allowed" in str(exc_info.value)


@pytest.mark.parametrize(
    "schema_type",
    [
        "list[dict]",
        "list[tuple]",
    ],
)
def test_validate_schema_type_generic_type_failure(schema_type):
    with pytest.raises(ValueError) as exc_info:
        validate_schema_type(schema_type)
    assert "Generic type" in str(exc_info.value) and "is not allowed for 'list'" in str(
        exc_info.value
    )
