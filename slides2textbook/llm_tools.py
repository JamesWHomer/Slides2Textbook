from dataclasses import dataclass
from functools import lru_cache
import logging
import os

from enum import Enum
from typing import NoReturn, Optional

from dotenv import load_dotenv
from google.genai.client import Client
from google.genai import types
from openai import OpenAI
from openai.types.responses import Response, ResponseUsage

from google import genai

from slides2textbook.llm_classes import LLM_Response, TokenCount
from slides2textbook.llm_classes import ModelProvider

logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

@lru_cache(maxsize=1)
def _openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY, max_retries=3)

@lru_cache(maxsize=1)
def _gemini_client() -> Client:
    return genai.Client(api_key=GEMINI_API_KEY)

@lru_cache(maxsize=1)
def _anthropic_client() -> NoReturn:
    raise NotImplementedError("Anthropic provider is not yet supported.")

def determine_provider(model_str: str) -> ModelProvider:
    split = model_str.split('/')
    if len(split) >= 2:
        return ModelProvider(split[0])
    else:
        if OPENAI_API_KEY:
            return ModelProvider.OPENAI
        if GEMINI_API_KEY:
            return ModelProvider.GEMINI
        if ANTHROPIC_API_KEY:
            return ModelProvider.ANTHROPIC
    raise ValueError(f"Cannot determine provider for {model_str!r}: no provider prefix and no API keys configured. Currently only 'openai', 'google' and 'anthropic' are supported.")

def determine_model(model_str: str) -> str:
    split = model_str.split('/')
    return split[-1] # TODO: Handle future providers that might amalgamate models. For example `huggingface/openai/gpt-5`

def generate_openai(developer: str, user: str, model: str = "gpt-5.2", effort: Optional[str] = None) -> LLM_Response:
    """Generate and return the output of a call to the OpenAI Responses api. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model: The model string used by the API for text generation.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        The complete, completed output of the API call. 
    """
    response = _openai_client().responses.create(
        model=model,
        reasoning={"effort": effort}, # effort of value None does not fail API.
        instructions=developer,
        input=user,
    )

    token_count = TokenCount()
    token_count.add_openai(response.usage)

    return LLM_Response(response.output_text, token_count)

def generate_gemini(developer: str, user: str, model: str = "gemini-3.0-flash", effort: Optional[str] = None) -> LLM_Response:
    """Generate and return the output of a call to the Google Gemini api. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model: The model string used by the API for text generation.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        The complete, completed output of the API call. 
    """

    response = _gemini_client().models.generate_content(
        model=model,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=developer,
            thinking_config=effort,
        ),
    )

    token_count = TokenCount()
    token_count.add_gemini(response.usage_metadata)

    return LLM_Response(response.text, token_count)

# print(generate_gemini("say poopers essay", "poopers make a poessay on poopers", "gemini-3-flash-preview", "minimal").token_count)

def generate(developer: str, user: str, model_str: str = "openai/gpt-5.2", effort: str = None) -> LLM_Response:
    """Generate and return the output of a call to the various API's. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model_str: The model string used by the API for text generation. Will determine model provider from model of format '<provider>/<model>'.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        The complete, completed output of the API call. 
    """
    model = determine_model(model_str)
    provider = determine_provider(model_str)
    match provider:
        case ModelProvider.OPENAI:
            return generate_openai(developer, user, model, effort)
        case ModelProvider.GEMINI:
            return generate_gemini(developer, user, model, effort)
        case ModelProvider.ANTHROPIC:
            raise NotImplementedError("Anthropic provider is not yet supported.")
        case _:
            raise ValueError(f"Unsupported model provider for model_str={model_str!r}: {provider!r}. Currently only 'openai', 'google' and 'anthropic' are supported.")
        