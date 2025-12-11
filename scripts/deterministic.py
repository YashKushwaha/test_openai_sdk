## Example from https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py

MODEL_NAME = 'qwen3:14b'
import mlflow
import asyncio

from pydantic import BaseModel

from agents import Agent, Runner, trace
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
"""
This example demonstrates a deterministic flow, where each step is performed by an agent.
1. The first agent generates a story outline
2. We feed the outline into the second agent
3. The second agent checks if the outline is good quality and if it is a scifi story
4. If the outline is not good quality or not a scifi story, we stop here
5. If the outline is good quality and a scifi story, we feed the outline into the third agent
6. The third agent writes the story
"""

from utils import setup_logging, get_async_client, look_up_item

setup_logging()

client  = get_async_client()
set_tracing_disabled(disabled=False)


story_outline_agent = Agent(
    name="story_outline_agent",
    instructions="Generate a very short story outline based on the user's input.",
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)


class OutlineCheckerOutput(BaseModel):
    good_quality: bool
    is_scifi: bool


outline_checker_agent = Agent(
    name="outline_checker_agent",
    instructions="Read the given story outline, and judge the quality. Also, determine if it is a scifi story.",
    output_type=OutlineCheckerOutput,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

story_agent = Agent(
    name="story_agent",
    instructions="Write a short story based on the given outline.",
    output_type=str,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

async def main():
    input_prompt = input("What kind of story do you want? ")

    # Ensure the entire workflow is a single trace
    with trace("Deterministic story flow"):
        # 1. Generate an outline
        outline_result = await Runner.run(
            story_outline_agent,
            input_prompt,
        )
        print("Outline generated")
        print(10*'==')
        print(outline_result.final_output)
        print(10*'==')
        # 2. Check the outline
        outline_checker_result = await Runner.run(
            outline_checker_agent,
            outline_result.final_output,
        )

        # 3. Add a gate to stop if the outline is not good quality or not a scifi story
        assert isinstance(outline_checker_result.final_output, OutlineCheckerOutput)
        if not outline_checker_result.final_output.good_quality:
            print("Outline is not good quality, so we stop here.")
            exit(0)

        if not outline_checker_result.final_output.is_scifi:
            print("Outline is not a scifi story, so we stop here.")
            exit(0)

        print("Outline is good quality and a scifi story, so we continue to write the story.")

        print(outline_result.final_output)
        # 4. Write the story
        story_result = await Runner.run(
            story_agent,
            outline_result.final_output,
        )
        print('Story: ')
        print(20*'=')
        print(f"{story_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())