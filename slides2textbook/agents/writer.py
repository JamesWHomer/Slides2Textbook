# Generate the full section text in md format.

from pydantic import BaseModel
from slides2textbook import llm_tools

class Section(BaseModel):
    markdown_text: str

    def __str__(self) -> str:
        return self.markdown_text

WRITER = (
    "You are a section writer and your task is to write a single section based on context, including previous sections, and a complete section plan. "
    "Base the section heavily on the context and plan; do not omit information or go off topic unless necessary. "
    "Respond only in Markdown. Do not output anything except the textbook. "
    "Do not include unnecessary artifacts such as page numbers or repeated headers. "
    "Do not include extra features such as exercises unless they are explicitly shown in the slides. "
    "You will not be able to see or create images. "
    "Do not start with a preamble; begin the textbook section immediately. Likewise do not end with a summary."
)

def generate_section(context: str, so_far_generated: str, section_plan, model="gpt-5", effort="high"):
    system = WRITER + "\n\n" + context + "\n\n" + so_far_generated
    prompt = str(section_plan)
    return llm_tools.generate(system, prompt, model=model, effort=effort, structured_output=Section)