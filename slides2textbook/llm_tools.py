# Handles OpenAI api calls.
import os
from typing import Optional, Type

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
client = OpenAI(api_key=OPENAI_API_KEY)

def context_creator(**contexts):
    context = ""
    for key, value in contexts.items():
        context += f"{key}:\n{value}\n\n"
    return context

def generate(system: str, prompt: str, model="gpt-5", effort="high", structured_output: Optional[Type[BaseModel]] = None):
    messages = [
        {
            "role": "developer",
            "content": [
                {
                    "type": "input_text",
                    "text": system
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": prompt
                }
            ]
        }
    ]

    base_args = {
        "model": model,
        "input": messages,
        "reasoning": {
            "effort": effort,
            # "summary": "auto"
        },
        "tools": [],
        "store": True,
        "include": [
            "reasoning.encrypted_content",
            "web_search_call.action.sources"
        ]
    }

    if structured_output is not None:
        if not issubclass(structured_output, BaseModel):
            raise TypeError("structured_output must be a Pydantic BaseModel subclass.")
        response = client.responses.parse(
            text_format=structured_output,
            **base_args
        )
        return response.usage.input_tokens, response.usage.output_tokens, response.output_parsed

    response = client.responses.create(
        text={
            "format": {
                "type": "text"
            },
            "verbosity": "high"
        },
        **base_args
    )
    return response.usage.input_tokens, response.usage.output_tokens, response.output_text