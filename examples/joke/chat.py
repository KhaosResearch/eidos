import json

import requests
import streamlit as st
from openai import OpenAI

# Configurate OpenAI's API
GPT_MODEL = "gpt-4.1-nano"
client = OpenAI()


tools = requests.get("http://0.0.0.0:8090/api/v1/functions/").json()


def execute_function_call(message) -> str:
    function_name = message.tool_calls[0].function.name
    params = json.loads(message.tool_calls[0].function.arguments)

    results = requests.post(
        f"http://0.0.0.0:8090/api/v1/execution/{function_name}",
        json=params,
    )

    return results


st.title("LLM GUI with tools powered by Eidos")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Walrus operator (:=)
# prompt = st.chat_input("Hello, how are you?")
# if prompt: # is not None
if prompt := st.chat_input("Hello, how are you?"):
    # Store message on session
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # LLM responds to the user prompts
    # Additionally, the LLM is capable of execution functions
    chat_completion = client.chat.completions.create(
        messages=st.session_state.messages,
        model=GPT_MODEL,
        tools=tools,
    )

    assistant_message = chat_completion.choices[0].message

    # If the LLM ask to execute a function
    if assistant_message.tool_calls:
        # Execute it
        results = execute_function_call(assistant_message)

        # Render debug function message
        with st.chat_message("function"):
            st.markdown(
                f"function='{assistant_message.tool_calls[0].function.name}', arguments='{assistant_message.tool_calls[0].function.arguments}', results='{results}'"
            )

        # Add it to the message log
        st.session_state.messages.append(
            {
                "role": "function",
                "tool_call_id": assistant_message.tool_calls[0].id,
                "name": assistant_message.tool_calls[0].function.name,
                "content": results,
            }
        )

        # Generate a model response
        chat_response = client.chat.completions.create(
            messages=st.session_state.messages,
            model=GPT_MODEL,
            tools=tools,
        )
        assistant_message = chat_response.choices[0].message

    # Render assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_message.content)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_message.content}
    )
