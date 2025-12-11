import json

import inspect

def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }

import hashlib


#@function_tool
def look_up_item(search_query):
    """Use to find item ID.
    Search query can be a description or keywords."""
    full_hash = hashlib.sha256(search_query.encode()).hexdigest()
    num = int(full_hash[:8], 16) % 100_000_000
    # return hard-coded item ID - in reality would be a lookup
    return f"item_{num}"

#@function_tool
def execute_refund(item_id, reason="not provided"):

    print("Summary:", item_id, reason) # lazy summary
    return "success"



def run_full_turn(client, system_message, tools, messages):

    num_init_messages = len(messages)
    messages = messages.copy()

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in tools]
        tools_map = {tool.__name__: tool for tool in tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system_message}] + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print assistant response
            print("Assistant:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools_map)

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return new messages =====
    return messages[num_init_messages:]


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"Assistant: {name}({args})")

    # call corresponding function with provided arguments
    return tools_map[name](**args)


system_message = (
    "You are a customer support agent for ACME Inc."
    "Always answer in a sentence or less."
    "Follow the following routine with the user:"
    "1. First, ask probing questions and understand the user's problem deeper.\n"
    " - unless the user has already provided a reason.\n"
    "2. Propose a fix (make one up).\n"
    "3. ONLY if not satisfied, offer a refund.\n"
    "4. If accepted, search for the ID and then execute refund."
    ""
)
import mlflow
from pathlib import Path

def setup_logging():
    current_dir = Path.cwd()
    project_root = current_dir#.parent
    mlflow_logs = project_root / "mlflow_logs"
    mlflow_logs.mkdir(exist_ok=True)
    db_path = mlflow_logs / "mlflow.db"
    print('MLFLOW DB -> ', db_path)
    #mlflow.set_tracking_uri(f"sqlite:///{db_path.resolve()}")
    mlflow.set_tracking_uri(f"file:///{mlflow_logs.resolve()}")

    mlflow.set_experiment("openai demo from website")
    mlflow.openai.autolog()

    import logging
    logging.basicConfig(level=logging.ERROR)

    # Silence migration logs
    logging.getLogger("mlflow").setLevel(logging.ERROR)
    logging.getLogger("alembic").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy").setLevel(logging.ERROR)


def get_client():
    from openai import OpenAI
    base_url = 'http://localhost:11434/v1'
    api_key = 'ollama'
    client  = OpenAI(base_url=base_url,api_key=api_key )
    return client

def check_os_type():
    import platform
    system = platform.system()

    if system == "Darwin":
        os_type = 'macOS'
    elif system == "Linux" and "WSL" in platform.release():
        os_type = "WSL"
    else:
        os_type = 'Other'

    return os_type



MODEL = 'qwen3:14b' if check_os_type() != 'macOS' else 'qwen3:1.7b'