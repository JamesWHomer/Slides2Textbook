# Handles OpenAI api calls.
import os
from dotenv import load_dotenv
from openai import OpenAI

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

def generate(system, prompt, model="gpt-5"):
    response = client.responses.create(
    model=model,
    input=[
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