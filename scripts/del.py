from agents import Agent, Runner, trace
from agents import Agent, ModelSettings

from openai.types.shared.reasoning import Reasoning
import io
import contextlib

buffer = io.StringIO()

with contextlib.redirect_stdout(buffer):
    help(Reasoning)

text = buffer.getvalue()

with open('Reasoning.md', 'w') as f:
    f.write(text)
