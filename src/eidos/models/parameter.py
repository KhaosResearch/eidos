from typing import Any, Optional

from pydantic import BaseModel, model_validator

from eidos.validation.type import (
    get_variable_type_name,
    parse_type_name,
    validate_schema_type,
)


class AiParameter(BaseModel):
    """This data model represents an AI parameter."""

    name: str
    description: str
    type: str
    options: Optional[list[Any]] = None
    regex: Optional[str] = None
    required: Optional[bool] = True
    default: Optional[Any] = None

    @model_validator(mode="before")
    def check_types(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validates AI parameter types against allowed types, ensuring options and default values are correctly typed.
        Recursive types and dict generic types are not validated.
        """
        type_str = values["type"]

        validate_schema_type(type_str)

        main_type, _ = parse_type_name(type_str)

        if values.get("regex") and values.get("options"):
            raise ValueError("Regex and options are mutually exclusive.")

        if not values.get("required") and values.get("default") is not None:
            if get_variable_type_name(values["default"]) != main_type:
                raise ValueError(
                    f"Default value must match the main type '{main_type}'."
                )

        if values.get("regex") is not None:
            if main_type != "str":
                raise ValueError(
                    "Regex patterns are only applicable to parameters of the string type."
                )

        options = values.get("options")

        if options is not None:
            if len(options) == 0:
                raise ValueError("The options list must not be empty.")
            if len(set(options)) != len(options):
                raise ValueError("All options must be unique.")
            for option in options:
                if get_variable_type_name(option) != main_type:
                    raise ValueError(
                        f"Each option in the list must be of the type '{main_type}', found type '{type(option).__name__}' for option '{option}'."
                    )

        return values
