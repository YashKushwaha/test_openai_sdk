import asyncio
import uuid

from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent

from agents import Agent, RawResponsesStreamEvent, Runner, TResponseInputItem, trace, set_tracing_disabled, OpenAIChatCompletionsModel
from utils import setup_logging, get_async_client, look_up_item

setup_logging()

client  = get_async_client()
set_tracing_disabled(disabled=False)

MODEL_NAME = 'qwen3:14b'

"""
This example shows the handoffs/routing pattern. The triage agent receives the first message, and
then hands off to the appropriate agent based on the language of the request. Responses are
streamed to the user.
"""

french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

hindi_agent = Agent(
    name="hindi_agent",
    instructions="You only speak Hindi. Reply using latin script. Devanagiri is not supported",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

hinglish_agent = Agent(
    name="hinglish_agent",
    instructions="You only speak Hinglish which is a mixture of Hindi mixed with English",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[ english_agent, hindi_agent, hinglish_agent],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)


async def main():
    # We'll create an ID for this conversation, so we can link each trace
    conversation_id = str(uuid.uuid4().hex[:16])

    msg = input("Hi! We speak multiple languages. How can I help? ")
    agent = triage_agent
    inputs: list[TResponseInputItem] = [{"content": msg, "role": "user"}]
    print(10*'-')
    print('Current Agent -> ', agent)
    print(10*'-')
    while True:
        # Each conversation turn is a single trace. Normally, each input from the user would be an
        # API request to your app, and you can wrap the request in a trace()
        #with trace("Routing example"):
        result = Runner.run_streamed(
            agent,
            input=inputs,
        )
        async for event in result.stream_events():
            if not isinstance(event, RawResponsesStreamEvent):
                continue
            data = event.data
            if isinstance(data, ResponseTextDeltaEvent):
                print(data.delta, end="", flush=True)
            elif isinstance(data, ResponseContentPartDoneEvent):
                print("\n")

        inputs = result.to_input_list()
        print("\n")

        user_msg = input("Enter a message: ")
        inputs.append({"content": user_msg, "role": "user"})
        agent = result.current_agent
        print(10*'-')
        print('Current Agent -> ', agent)
        print(10*'-')

if __name__ == "__main__":
    asyncio.run(main())