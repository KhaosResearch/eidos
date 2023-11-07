import builtins

from pydantic import BaseModel, Field, create_model
from pydantic_core import PydanticUndefined

from eidos.models.parameter import AiParameter
from eidos.validation.type import split_type_from_generic


def load_model(function_: dict) -> BaseModel:
    """Load the pydantic model of a function from its JSON definition.

    This pydantic model is compatible with OpenAI functions if exported as JSON schema.

    Example:
    ```
    function_model = load_model(function)
    function_model.model_json_schema()
    ```

    Args:
        function_ (dict): JSON definition of the function.

    Returns:
        BaseModel: Pydantic model of the function.
    """
    parameters = [
        AiParameter.model_validate(parameter) for parameter in function_["parameters"]
    ]

    parameters_dict = {}
    for v in parameters:
        json_schema_extra = {}
        if v.options:
            json_schema_extra["enum"] = v.options

        type_ = getattr(
            builtins,
            split_type_from_generic(v.type)[
                0
            ],  # OpenAI does not support generic types, remove it
        )

        # PydanticUndefined is used to mark parameters as not required
        default_ = PydanticUndefined
        if not v.required:
            default_ = v.default

        parameters_dict[v.name] = (
            type_,
            Field(
                default=default_,  # Set a default value to mark them as not required
                description=v.description,
                pattern=v.regex,
                json_schema_extra=json_schema_extra,
            ),
        )

    ai_function = create_model(
        function_["name"],
        **parameters_dict,
    )

    return ai_function
