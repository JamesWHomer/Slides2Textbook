# Handles OpenAI api calls.
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = ("You are a textbook chapter creator. Given a possibly badly structured markdown file likely created from pdf's/slides "
    "and missing information such as images, you will attempt to the best of your ability to create a high quality textbook chapter "
    "of the slides/notes in the markdown file provided, aiming to best educate the reader. "
    "Base the textbook heavily off of the slides, do not miss any information or go too off topic from the textbook unless necessary. "
    "Respond in markdown format and assume that your response will be included in the chapter, "
    "so do not respond with anything but the textbook. "
    "Do not include unecessary artifacts from the previous format such as page numbers or repeated information such as headers. "
    "Do not include extra features such as exercises unless they are explicitely shown in the slides. Remember your tasks is to create a chapter based on slides, not a chapter itself. "
    "Note that a transcript will also possibly be attached from any lecture using that slide. Use the information to augment and determine what other information to include. "
    "Note that you will not able to see any images or create any images. "
    "The textbook chapter should be considered standalone. "
    "Do not start with a preamble, go into the textbook chapter immediately. "
    )

def context_creator(**contexts):
    context = ""
    for key, value in contexts.items():
        context += f"{key}:\n{value}\n\n"
    return context

def to_chapter(context):
    response = client.responses.create(
    model="gpt-5-nano",
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