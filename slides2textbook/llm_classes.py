from dataclasses import dataclass

from openai.types.responses import ResponseUsage


@dataclass
class TokenCount:
    input_tokens: int = 0
    cached_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    
    def add_openai(self, usage: ResponseUsage) -> None:
        self.input_tokens += usage.input_tokens
        if usage.input_tokens_details:
            self.cached_tokens += usage.input_tokens_details.cached_tokens
        self.output_tokens += usage.output_tokens
        if usage.output_tokens_details:
            self.reasoning_tokens += usage.output_tokens_details.reasoning_tokens

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