from typing import Any, Optional

from pydantic import BaseModel, model_validator


class AiParameter(BaseModel):
    """This data model represents an AI parameter."""

    name: str
    description: str
    type: str
    options: Optional[list[Any]]
    regex: Optional[str]

    @model_validator(mode="before")
    def _check_types(cls, values: dict) -> dict:
        """Check that the type is one of the allowed ones and
        that the options are of the correct type.

        """
        if values["regex"] is not None and values["options"] is not None:
            raise ValueError("Regex and options are mutually exclusive")

        if values["type"] not in ["str", "int", "float", "bool", "list", "dict"]:
            raise ValueError(
                "Type must be one of str, int, float, bool, list or dict. "
                f"Currently, it is {values['type']}"
            )

        type_ = eval(values["type"])

        if values["options"] is not None:
            if len(values["options"]) == 0:
                raise ValueError("Options must be a non-empty list")
            if len(set(values["options"])) != len(values["options"]):
                raise ValueError("Options must be a list of unique values")

            for option in values["options"]:
                if not (type_ == type(option)):
                    raise ValueError(
                        f"Options must be a list of {values['type']}, "
                        "but {option} is {type(option)}"
                    )
        return values
