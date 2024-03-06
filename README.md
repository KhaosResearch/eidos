# eidos:  Validation and execution of AI functions

eidos is an API for validating and executing AI functions. It aims to be a generic API to serve as a common interface to allow execution of functions by LLMs.

## Install

From source:

```bash
git clone git@github.com:KhaosResearch/eidos.git
cd eidos
pip install -e .
```

Or directly from GitHub:

```bash
pip install "eidos @ git+ssh://git@github.com/KhaosResearch/eidos.git
```

## Run

Run the API with the following command:

```bash
uvicorn src.eidos.main:app --host 0.0.0.0 --port 8090 --reload
```

You can override the default configuration by setting [environment variables](src/eidos/settings.py).

## Function definition

Functions are defined as a json that is then transpiled to OpenAI or whatever new format emerges. Currently, the eidos description of the function has the following fields:
- `name`: Name of the function.
- `description`: Description of the function.
- `module`: Full qualified name of the module and the function to execute. It ***must*** be importable in eidos.
- `parameters`: Schema of the parameters that the function accepts.
    - `name`: Name of the parameter.
    - `type`: Type of the parameter in Python notation. Example: `str`, `int`, `float`... List with a generic type are supported.
    - `description`: Description of the parameter.
    - `options`: List of options that the parameter accepts. Similar to a enum. Example: `["option1", "option2"]`. Can't be used along with `regex`.
    - `regex`: For string parameters, a regex can be specified to validate the input. Can't be used along with `options`.
    - `default`: Default value of the parameter. It is ignored if the parameter is required. Default is `null` or None.
    - `required`: If the parameter is required or not. Default is `false`.
- `response`: Schema of the response of the function. Keys are parameter names and values are the type of the parameter.

Example function definition:
```json
{
    "name": "salute",
    "description": "This function can be used to salute someone.",
    "module": "eidos.functions.core.salute",
    "parameters": [
        {
            "name": "who",
            "type": "str",
            "description": "Name of whom to salute. o7",
            "options": null,
            "regex": null,
            "default": null,
            "required": true
        }
    ],
    "response": {
        "msg": "str"
    }
}
```

A very simple example of a function is the Salute function: Receives a name and returns a salute. The definition of the function can be found at [functions/salute.json](functions/salute.json) and the code at [src/eidos/functions/core.py](src/eidos/functions/core.py).

## Testing

A [Postman](https://www.postman.com/downloads/) collection is provided for automated integration testing of the API. You can find more details at [tests](tests).