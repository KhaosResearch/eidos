# eidos:  Validation and execution of AI functions

eidos is an API for validating and executing AI functions. It aims to be a generic API to serve as a common interface to allow execution of functions by LLMs.

## Why "Eidos"?
The name "Eidos" was chosen for this project to symbolize our dedication to achieving perfection and validating idealized forms or concepts. In Greek mythology, Eidos represented these perfected forms. Similarly, our project aims to embody and represent excellence in its pursuit of its objectives.

## Installation
To install eidos:

```bash
git clone git@github.com:KhaosResearch/eidos.git
cd eidos
pip install .
# or to install without cloning
pip install "eidos @ git+ssh://git@github.com/KhaosResearch/eidos.git
```

## Deployment
Configuration can be made by enviroment variables, a full list of enviroment variables can be found in the [src/eidos/settings.py](src/eidos/settings.py) file.
```bash
python -m eidos server
```

## Function definition
Functions are defined as a json that is then transpiled to OpenAI or whatever new format emerges. Currently, the eidos description of the function has the following fields:
- `name`: Name of the function.
- `description`: Description of the function.
- `module`: Full qualified name of the module and the function to execute. It ***must*** be importable in eidos.
- `parameters`: Schema of the parameters that the function accepts.
    - `name`: Name of the parameter.
    - `type`: Type of the parameter in Python notation. Example: `str`, `int`, `float`...
    - `description`: Description of the parameter.
    - `options`: List of options that the parameter accepts. Similar to a enum. Example: `["option1", "option2"]`.
    - `regex`: For string parameters, a regex can be specified to validate the input.
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
            "regex": null
        }
    ],
    "response": {
        "msg": "str"
    }
}
```


Two very simple examples of functions are the following:
- Salute function: Receives a name and returns a salute. The definition of the function can be found at [functions/salute.json](functions/salute.json) and the code at [src/eidos/functions/core.py](src/eidos/functions/core.py).
- Geocoding function: Receives a location and returns the coordinates. The definition of the function can be found at [functions/geocode.json](functions/geocode.json) and the code at [src/eidos/functions/core.py](src/eidos/functions/core.py).

## Testing the API
A [Postman](https://www.postman.com/downloads/) collection is provided for automated integration testing of the API. You can find more details at [tests](tests).