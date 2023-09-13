import json
import os

import openai

from eidos.execution import import_function
from eidos.functions.classification import zero_shot_classification
from eidos.models.function import load_model

function = json.load(open("functions/hello_world.json", "r"))
function_model = load_model(function)

# Load your API key from an environment variable or secret management service
openai.api_key = os.environ["OPENAI_API_KEY"]

# Examples of user inputs with different characteristics
user_inputs = [
    "Hello Bot, I am world! Nice to meet you!",
    "Today is a sunny day, how old are you?",
    "The table is made of wood.",
]

for user_input in user_inputs:
    label, _ = zero_shot_classification(user_input, candidate_labels=["Salute", "Information"])

    # Only allow tool execution if the intent is QuestionRequiresAnswer
    if label == "Salute":
        functions = [
            {
                "name": function["name"],
                "description": function["description"],
                "parameters": function_model.model_json_schema(),
            }
        ]

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": user_input},
            ],
            functions=functions,
            function_call="auto",
        )
    else:
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": user_input},
            ],
        )

    # Execute the function if it is a function call or print the answer
    message = chat_completion["choices"][0]["message"]
    if "function_call" in message:
        function_name = message["function_call"]["name"]

        # TODO: search function by name and extract its module
        if function["name"] == function_name:
            module = function["module"]

        print(f"\tExecuting function {function_name}...")

        kwargs = json.loads(message["function_call"]["arguments"])
        result = import_function(module)(**kwargs)
    else:
        print("\Response:", message["content"])

    print(f"\tPrompt token usage: {chat_completion['usage']['prompt_tokens']}")
    print(f"\tAnswer token usage: {chat_completion['usage']['completion_tokens']}")

