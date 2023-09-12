import builtins

from pydantic import BaseModel, Field, create_model

from eidos.models.parameter import AiParameter


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

    ai_function = create_model(
        function_["name"],
        **{
            v.name: (
                getattr(builtins, v.type),
                Field(
                    description=v.description,
                    pattern=v.regex,
                    json_schema_extra={"enum": v.options} if v.options else {},
                ),
            )
            for v in parameters
        },
    )

    return ai_function
