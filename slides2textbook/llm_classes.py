class LLM_Response:
    """
    Container to cleanly return an LLM Response.
    """
    def __init__(self, output_text: str, token_count: TokenCount):
        self.output_text = output_text
        self.token_count: TokenCount = TokenCount()
        self.token_count.add()