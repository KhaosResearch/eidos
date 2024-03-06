import pytest
from eidos.models.function import load_model
from eidos.models.parameter import AiParameter
from pydantic import ValidationError


def test_load_model_with_minimal_valid_input():
    json_definition = {
        "name": "TestFunction",
        "parameters": [
            {
                "name": "param1",
                "description": "This is a test parameter.",
                "type": "str",
                "required": True,
            }
        ],
    }
    model = load_model(json_definition)
    assert model.model_fields["param1"].annotation == str
    assert model.model_fields["param1"].is_required() is True


def test_load_model_with_complex_input():
    json_definition = {
        "name": "ComplexFunction",
        "parameters": [
            {
                "name": "param1",
                "description": "This is a test parameter.",
                "type": "str",
                "required": False,
                "default": "default_value",
                "regex": "^[a-zA-Z]+$",
            },
            {
                "name": "param2",
                "description": "This is a test parameter.",
                "type": "int",
                "required": True,
                "options": [1, 2, 3],
            },
        ],
    }
    model = load_model(json_definition)
    assert model.model_fields["param1"].default == "default_value"
    assert model.model_fields["param1"].metadata[0].pattern == "^[a-zA-Z]+$"
    assert model.model_fields["param2"].json_schema_extra["enum"] == [1, 2, 3]


def test_load_model_with_invalid_type():
    json_definition = {
        "name": "InvalidTypeFunction",
        "parameters": [
            {
                "name": "param1",
                "description": "This is a test parameter.",
                "type": "unknown_type",
                "required": True,
            }
        ],
    }
    with pytest.raises(ValueError):
        load_model(json_definition)


def test_load_model_with_required_and_optional_fields():
    json_definition = {
        "name": "RequiredOptionalFunction",
        "parameters": [
            {
                "name": "required_param",
                "description": "This is a test parameter.",
                "type": "str",
                "required": True,
            },
            {
                "name": "optional_param",
                "description": "This is a test parameter.",
                "type": "int",
                "required": False,
                "default": 10,
            },
        ],
    }
    model = load_model(json_definition)
    assert model.model_fields["required_param"].is_required() is True
    assert model.model_fields["optional_param"].is_required() is not True
    assert model.model_fields["optional_param"].default == 10


def test_load_model_with_defaults():
    json_definition = {
        "name": "DefaultFunction",
        "parameters": [
            {
                "name": "param",
                "description": "This is a test parameter.",
                "type": "str",
                "required": False,
                "default": "hello",
            }
        ],
    }
    model = load_model(json_definition)
    instance = model()
    assert instance.param == "hello"


def test_validate_ai_parameter_types_valid_input():
    values = {
        "type": "str",
        "default": "example",
        "required": False,
    }
    expected = values
    assert AiParameter.check_types(values) == expected


def test_validate_ai_parameter_types_regex_and_options_exclusion():
    values = {
        "type": "str",
        "regex": ".*",
        "options": ["one", "two"],
    }
    with pytest.raises(ValidationError):
        AiParameter(**values)


def test_validate_ai_parameter_types_default_type_matching():
    values = {
        "type": "int",
        "default": "not_an_int",
        "required": False,
    }
    with pytest.raises(ValidationError):
        AiParameter(**values)


def test_validate_ai_parameter_types_regex_applicability():
    values = {
        "type": "int",  # Regex should only be applicable to strings
        "regex": ".*",
    }
    with pytest.raises(ValidationError):
        AiParameter(**values)


def test_validate_ai_parameter_types_options_list_not_empty():
    values = {
        "type": "str",
        "options": [],
    }
    with pytest.raises(ValidationError):
        AiParameter(**values)


def test_validate_ai_parameter_types_options_unique():
    values = {
        "type": "str",
        "options": ["duplicate", "duplicate"],
    }
    with pytest.raises(ValidationError):
        AiParameter(**values)


def test_validate_ai_parameter_types_options_type_matching():
    values = {
        "type": "str",
        "options": ["valid", 123],  # 123 is not a string
    }
    with pytest.raises(ValidationError):
        AiParameter(**values)
