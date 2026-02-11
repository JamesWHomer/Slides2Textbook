from dataclasses import dataclass
from functools import lru_cache
import os

from enum import Enum

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import Response, ResponseUsage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class ModelProvider(Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"

@lru_cache(maxsize=1)
def _openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY, max_retries=3)

@lru_cache(maxsize=1)
def _google_client() -> OpenAI:
    pass

@lru_cache(maxsize=1)
def _anthropic_client() -> OpenAI:
    pass

def determine_provider(model_str: str) -> ModelProvider:
    split = model_str.split('/')
    if len(split) >= 2:
        return ModelProvider(split[0])
    else:
        if OPENAI_API_KEY:
            return ModelProvider.OPENAI
        if GOOGLE_API_KEY:
            return ModelProvider.GOOGLE
        if ANTHROPIC_API_KEY:
            return ModelProvider.ANTHROPIC
    raise ValueError(f"Cannot determine provider for {model_str!r}: no provider prefix and no API keys configured. Currently only 'openai', 'google' and 'anthropic' are supported.")

def determine_model(model_str: str) -> str:
    split = model_str.split('/')
    return split[-1]

def generate_openai(developer: str, user: str, model: str = "gpt-5.2", effort: str = None) -> Response:
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

def generate(developer: str, user: str, model_str: str = "openai/gpt-5.2", effort: str = None) -> Response:
    """Generate and return the output of a call to the various API's. No streaming supported.

    Args:
        developer: Developer message also known as System Prompt. Instructions that the LLM follows closely.
        user: User prompt which in our usecase includes context that the LLM can use to generate text. Used less for instruction following than developer.
        model: The model string used by the API for text generation. Will determine model provider from model of format '<provider>/<model>'.
        effort: The reasoning/thinking effort that the model uses. For example none/minimal/low/medium/high. Higher effort -> Higher latency.

    Returns:
        The complete, completed output of the API call. 
    """
    model = determine_model(model_str)
    provider = determine_provider(model_str)
    match provider:
        case ModelProvider.OPENAI:
            return generate_openai(developer, user, model, effort)
        case ModelProvider.GOOGLE:
            raise NotImplementedError("Google provider is not yet supported.")
        case ModelProvider.ANTHROPIC:
            raise NotImplementedError("Anthropic provider is not yet supported.")
        case _:
            raise ValueError(f"Unsupported model provider for model_str={model_str!r}: {provider!r}. Currently only 'openai', 'google' and 'anthropic' are supported.")
        

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