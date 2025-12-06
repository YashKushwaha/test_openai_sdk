import json
from pydantic import BaseModel
from scripts.utils import MODEL, function_to_schema
from utils import execute_refund

from utils import system_message, setup_logging, get_client

setup_logging()

# Customer Service Routine
client = get_client()


class Agent(BaseModel):
    name: str = "Agent"
    model: str = MODEL
    instructions: str = "You are a helpful Agent"
    tools: list = []

def run_full_turn(agent, messages):
    client = get_client()
    num_init_messages = len(messages)
    messages = messages.copy()

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in agent.tools]
        tools_map = {tool.__name__: tool for tool in agent.tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": agent.instructions}] + messages,
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

def execute_refund(item_name):
    return "success"

def place_order(item_name):
    return "success"


if __name__ == '__main__':

    refund_agent = Agent(
        name="Refund Agent",
        instructions="You are a refund agent. Help the user with refunds.",
        tools=[execute_refund],
    )

    sales_assistant = Agent(
        name="Sales Assistant",
        instructions="You are a sales assistant. Sell the user a product.",
        tools=[place_order],
    )


    messages = []
    user_query = "Place an order for a black boot."
    print("User:", user_query)
    messages.append({"role": "user", "content": user_query})

    response = run_full_turn(sales_assistant, messages) # sales assistant
    messages.extend(response)

    user_query = "Actually, I want a refund." # implicitly refers to the last item
    print("User:", user_query)
    messages.append({"role": "user", "content": user_query})
    response = run_full_turn(refund_agent, messages) # refund agent