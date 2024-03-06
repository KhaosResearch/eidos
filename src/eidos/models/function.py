import builtins

from pydantic import BaseModel, Field, create_model

from eidos.models.parameter import AiParameter
from eidos.validation.type import parse_type_name


def load_model(fn: dict) -> BaseModel:
    """Load a Pydantic model from a function's JSON definition.

    This function creates a Pydantic model dynamically based on a provided JSON schema
    representation of a function's parameters.

    Example:
    >> function_model = load_model(function)
    >> function_model.model_json_schema()

    Args:
        fn (dict): JSON definition of the function.

    Returns:
        BaseModel: A dynamically created Pydantic model.
    """
    parameters = [
        AiParameter.model_validate(param) for param in fn.get("parameters", [])
    ]
    parameters_dict = {}
    for param in parameters:
        json_schema_extra = {"enum": param.options} if param.options else {}

        # Resolve a type string to a Python type object.
        # Note: OpenAI does not support custom generic types, so we only need to handle built-in types.
        type_ = getattr(
            builtins,
            parse_type_name(param.type)[0],
        )

        parameters_dict[param.name] = (
            type_,
            Field(
                default=(... if param.required else param.default),
                description=param.description,
                pattern=param.regex,
                json_schema_extra=json_schema_extra,
            ),
        )

    return create_model(fn["name"], **parameters_dict)
