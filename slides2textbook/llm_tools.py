from dataclasses import dataclass
from functools import lru_cache
import logging
import mimetypes
import os
import base64
import time

from enum import Enum
from pathlib import Path
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
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_POLL_INTERVAL_SECONDS = 5
OPENAI_PENDING_STATUSES = {"queued", "in_progress"}
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

@lru_cache(maxsize=1)
def _openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY, max_retries=3)

@lru_cache(maxsize=1)
def _gemini_client() -> Client:
    return genai.Client(api_key=GEMINI_API_KEY)

@lru_cache(maxsize=1)
def _anthropic_client() -> NoReturn:
    raise NotImplementedError("Anthropic provider is not yet supported.")

@lru_cache(maxsize=1)
def _openrouter_client() -> OpenAI:
    return OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL, max_retries=3)

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
        if OPENROUTER_API_KEY:
            return ModelProvider.OPENROUTER
    raise ValueError(f"Cannot determine provider for {model_str!r}: no provider prefix and no API keys configured. Currently only 'openai', 'google', 'anthropic' and 'openrouter' are supported.")

def determine_model(model_str: str) -> str:
    # Strip only the provider prefix; OpenRouter model IDs themselves contain
    # slashes (e.g. 'openrouter/openai/gpt-5.4' -> 'openai/gpt-5.4').
    _, sep, rest = model_str.partition('/')
    return rest if sep else model_str

def _wait_for_openai_response(response: Response) -> Response:
    while response.status in OPENAI_PENDING_STATUSES:
        logger.debug(
            "OpenAI background response %s is %s; polling again in %s seconds.",
            response.id,
            response.status,
            OPENAI_POLL_INTERVAL_SECONDS,
        )
        time.sleep(OPENAI_POLL_INTERVAL_SECONDS)
        response = _openai_client().responses.retrieve(response.id)

    if response.status != "completed":
        details = response.error or response.incomplete_details
        raise RuntimeError(
            f"OpenAI response {response.id} ended with "
            f"status={response.status!r}: {details}"
        )

    return response

def generate_openai(developer: str, user: str, model: str = "gpt-5.4", effort: Optional[str] = None) -> LLM_Response:
    """Generate and return the output of an OpenAI background Response.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model: The model string used by the API for text generation.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        An LLM_Response Object. 
    """
    response = _openai_client().responses.create(
        model=model,
        reasoning={"effort": effort}, # effort of value None does not fail API.
        instructions=developer,
        input=user,
        background=True,
        store=True,
    )
    response = _wait_for_openai_response(response)

    token_count = TokenCount()
    if response.usage is None:
        raise RuntimeError(
            f"Completed OpenAI response {response.id} did not include usage data."
        )
    token_count.add_openai(response.usage)

    return LLM_Response(response.output_text, token_count)

EFFORT_TO_THINKING_CONFIG = {
    None:      None,
    "none":    types.ThinkingConfig(thinking_budget=0),
    "minimal": types.ThinkingConfig(thinking_budget=1024),
    "low":     types.ThinkingConfig(thinking_budget=4096),
    "medium":  types.ThinkingConfig(thinking_budget=8192),
    "high":    types.ThinkingConfig(thinking_budget=-1),
}

def generate_gemini(developer: str, user: str, model: str = "gemini-3.0-flash", effort: Optional[str] = None) -> LLM_Response:
    """Generate and return the output of a call to the Google Gemini api. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model: The model string used by the API for text generation.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        An LLM_Response Object.
    """
    thinking_config = EFFORT_TO_THINKING_CONFIG.get(effort)

    response = _gemini_client().models.generate_content(
        model=model,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=developer,
            thinking_config=thinking_config,
        ),
    )

    token_count = TokenCount()
    token_count.add_gemini(response.usage_metadata)

    return LLM_Response(response.text, token_count)

def _openrouter_chat(messages: list[dict], model: str, effort: Optional[str] = None) -> LLM_Response:
    """Send a chat completion request to OpenRouter and wrap the result."""
    extra_body = {"reasoning": {"effort": effort}} if effort else None

    response = _openrouter_client().chat.completions.create(
        model=model,
        messages=messages,
        extra_body=extra_body,
    )

    if not response.choices or response.choices[0].message.content is None:
        raise RuntimeError(
            f"OpenRouter response {response.id} for model {model!r} did not include text output."
        )

    token_count = TokenCount()
    if response.usage is not None:
        token_count.add_openrouter(response.usage)
    else:
        token_count.supported = False

    return LLM_Response(response.choices[0].message.content, token_count)

def generate_openrouter(developer: str, user: str, model: str = "openai/gpt-5.4", effort: Optional[str] = None) -> LLM_Response:
    """Generate and return the output of a call to the OpenRouter API. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model: The OpenRouter model ID, e.g. 'openai/gpt-5.4' or 'anthropic/claude-sonnet-5'.
        effort: The reasoning/thinking effort forwarded to OpenRouter (e.g. low/medium/high). Only supported by some models.

    Returns:
        An LLM_Response Object.
    """
    return _openrouter_chat(
        [
            {"role": "system", "content": developer},
            {"role": "user", "content": user},
        ],
        model,
        effort,
    )

def generate(developer: str, user: str, model_str: str = "openai/gpt-5.4", effort: str = None) -> LLM_Response:
    """Generate and return the output of a call to the various API's. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model_str: The model string used by the API for text generation. Will determine model provider from model of format '<provider>/<model>'.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        An LLM_Response Object. 
    """
    model = determine_model(model_str)
    provider = determine_provider(model_str)
    match provider:
        case ModelProvider.OPENAI:
            return generate_openai(developer, user, model, effort)
        case ModelProvider.GEMINI:
            return generate_gemini(developer, user, model, effort)
        case ModelProvider.OPENROUTER:
            return generate_openrouter(developer, user, model, effort)
        case ModelProvider.ANTHROPIC:
            raise NotImplementedError("Anthropic provider is not yet supported.")
        case _:
            raise ValueError(f"Unsupported model provider for model_str={model_str!r}: {provider!r}. Currently only 'openai', 'google', 'anthropic' and 'openrouter' are supported.")
        
def image_analysis(instruction: str, image_path: str | Path, model_str: str = "openai/gpt-5.4", effort: str = None) -> LLM_Response:
    """Analyze an image with various API's. No streaming supported.

    Args:
        instruction: Instructions for what the model should do with the image.
        model_str: The model string used by the API for text generation. Will determine model provider from model of format '<provider>/<model>'.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        An LLM_Response Object. 
    """
    model = determine_model(model_str)
    provider = determine_provider(model_str)
    match provider:
        case ModelProvider.OPENAI:
            return openai_image_analysis(instruction, image_path, model, effort)
        case ModelProvider.OPENROUTER:
            return openrouter_image_analysis(instruction, image_path, model, effort)
        case ModelProvider.GEMINI:
            raise NotImplementedError("Gemini provider is not yet supported for image understanding.")
        case ModelProvider.ANTHROPIC:
            raise NotImplementedError("Anthropic provider is not yet supported for image understanding.")
        case _:
            raise ValueError(f"Unsupported model provider for model_str={model_str!r}: {provider!r}. Currently only 'openai', 'google', 'anthropic' and 'openrouter' are supported.")


def _image_data_url(image_path: str | Path) -> str:
    """Read an image file and return it as a base64 data URL."""
    image_path = Path(image_path)

    mime_type, _ = mimetypes.guess_type(image_path.name)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:{mime_type};base64,{base64_image}"


def openai_image_analysis(instruction: str, image_path: str | Path, model: str = "gpt-5.4", effort: str = None) -> LLM_Response:
    image_data_url = _image_data_url(image_path)

    response = _openai_client().responses.create(
        model=model,
        reasoning={"effort": effort},
        input=[
            {
                "role": "developer",
                "content": instruction
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": image_data_url,
                    },
                ],
            }
        ],
    )

    token_count = TokenCount()
    token_count.add_openai(response.usage)

    return LLM_Response(response.output_text, token_count)


def openrouter_image_analysis(instruction: str, image_path: str | Path, model: str = "openai/gpt-5.4", effort: str = None) -> LLM_Response:
    image_data_url = _image_data_url(image_path)

    return _openrouter_chat(
        [
            {"role": "system", "content": instruction},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_data_url},
                    },
                ],
            },
        ],
        model,
        effort,
    )
