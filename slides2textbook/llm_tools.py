# Handles OpenAI api calls.
import os
from dotenv import load_dotenv
from openai import OpenAI
from slides2textbook import prompt_builder as pb

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = pb.build_system_prompt()

def context_creator(**contexts):
    context = ""
    for key, value in contexts.items():
        context += f"{key}:\n{value}\n\n"
    return context

def to_chapter(context):
    response = client.responses.create(
    model="gpt-5",
    input=[
        {
        "role": "developer",
        "content": [
            {
            "type": "input_text",
            "text": SYSTEM_PROMPT
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "input_text",
            "text": context
            }
        ]
        }
    ],
    text={
        "format": {
        "type": "text"
        },
        "verbosity": "high"
    },
    reasoning={
        "effort": "high",
        "summary": "auto"
    },
    tools=[],
    store=True,
    include=[
        "reasoning.encrypted_content",
        "web_search_call.action.sources"
    ]
    )
    return response.output_text