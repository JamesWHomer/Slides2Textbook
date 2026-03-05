from dataclasses import dataclass

from google.genai import types
from openai.types.responses import ResponseUsage

from enum import Enum


class ModelProvider(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"

    @classmethod
    def _missing_(cls, value):
        aliases = {"google": cls.GEMINI}
        return aliases.get(value)

@dataclass
class TokenCount:
    supported: bool = True

    input_tokens: int = 0
    cached_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0

    def add(self, token_count) -> None:
        if not self.supported:
            return
        self.input_tokens += token_count.input_tokens
        self.cached_tokens += token_count.cached_tokens
        self.output_tokens += token_count.output_tokens
        self.reasoning_tokens += token_count.reasoning_tokens
    
    def add_openai(self, usage: ResponseUsage) -> None:
        if not self.supported:
            return
        self.input_tokens += usage.input_tokens
        if usage.input_tokens_details:
            self.cached_tokens += usage.input_tokens_details.cached_tokens
        self.output_tokens += usage.output_tokens
        if usage.output_tokens_details:
            self.reasoning_tokens += usage.output_tokens_details.reasoning_tokens

    def add_gemini(self, usage: types.GenerateContentResponseUsageMetadata):
        if not self.supported:
            return
        self.input_tokens += usage.prompt_token_count
        if usage.cached_content_token_count:
            self.cached_tokens += usage.cached_content_token_count
        self.output_tokens += usage.candidates_token_count
        if usage.thoughts_token_count:
            self.reasoning_tokens += usage.thoughts_token_count
        

    def add_anthropic(self):
        if not self.supported:
            return
        raise NotImplementedError

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def __str__(self):
        return f"(Input Tokens: {self.input_tokens}, Cached Tokens: {self.cached_tokens}, Output Tokens: {self.output_tokens}, Reasoning Tokens: {self.reasoning_tokens}, Total Tokens: {self.total_tokens})"


class LLM_Response:
    """
    Container to cleanly return an LLM Response.
    """
    def __init__(self, output_text: str, token_count: TokenCount):
        self.output_text = output_text
        self.token_count = token_count