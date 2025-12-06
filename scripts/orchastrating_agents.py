from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel
from typing import Optional
import json

import mlflow
from pathlib import Path

from utils import look_up_item, execute_refund, run_full_turn

from utils import system_message, setup_logging, get_client

setup_logging()


# Customer Service Routine
client = get_client()

tools = [execute_refund, look_up_item]
messages = []
while True:
    user = input("User: ")
    if not user: break
    messages.append({"role": "user", "content": user})
    new_messages = run_full_turn(client, system_message, tools, messages)
    messages.extend(new_messages)