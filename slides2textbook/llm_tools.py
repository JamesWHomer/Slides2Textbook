# Handles OpenAI api calls.
from dataclasses import dataclass
import os
from typing import Optional, Type

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import Response, ResponseUsage
from pydantic import BaseModel

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
client = OpenAI(api_key=OPENAI_API_KEY, max_retries=3)

def generate(developer: str, user: str, model: str = "gpt-5.2", effort: str = None) -> Response:
    """Generate and return the output of a call to the OpenAI Responses api. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model: The model string used by the API for text generation.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        The complete, completed output of the API call. 
    """
    return _openai_client().responses.create(
        model=model,
        reasoning={"effort": effort},
        instructions=developer,
        input=user,
    )

@dataclass
class TokenCount:
    input_tokens: int = 0
    cached_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    
    def add(self, usage: ResponseUsage) -> None:
        self.input_tokens += usage.input_tokens
        self.cached_tokens += usage.input_tokens_details.cached_tokens
        self.output_tokens += usage.output_tokens
        self.reasoning_tokens += usage.output_tokens_details.reasoning_tokens

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def __str__(self):
        return f"(Input Tokens: {self.input_tokens}, Cached Tokens: {self.cached_tokens}, Output Tokens: {self.output_tokens}, Reasoning Tokens: {self.reasoning_tokens}, Total Tokens: {self.total_tokens})"