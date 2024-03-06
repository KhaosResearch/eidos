import json

import pytest
from eidos.utils import import_function


def test_import_function_success():
    assert (
        import_function("json.loads") == json.loads
    ), "Should import the json.loads function successfully"


def test_import_function_module_not_exist():
    with pytest.raises(ImportError):
        import_function("nonexistent.module.func")


def test_import_function_function_not_exist():
    with pytest.raises(AttributeError):
        import_function("json.nonexistent_func")


@pytest.mark.parametrize(
    "module_str",
    [
        "justamodule",
        "",
    ],
)
def test_import_function_invalid_module_string(module_str):
    with pytest.raises(ValueError) as exc_info:
        import_function(module_str)
    assert "You can't import built-in modules" in str(exc_info.value)
