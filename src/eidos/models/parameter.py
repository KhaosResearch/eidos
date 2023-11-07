from typing import Any, Optional

from pydantic import BaseModel, model_validator

from eidos.validation.type import check_ai_parameter_types


class AiParameter(BaseModel):
    """This data model represents an AI parameter."""

    name: str
    description: str
    type: str
    options: Optional[list[Any]]
    regex: Optional[str]
    required: Optional[bool] = True
    default: Optional[Any] = None

    @model_validator(mode="before")
    def _check_types(cls, values: dict) -> dict:
        """Check that the type is one of the allowed ones and
        that the options are of the correct type.

        More documentation about validation can be found at `eidos.validation`
        """
        return check_ai_parameter_types(values)
