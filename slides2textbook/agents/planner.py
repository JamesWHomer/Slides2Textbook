from pydantic import BaseModel
from slides2textbook import llm_tools

class ChapterPlan(BaseModel):
    section_names: list[str]
    section_plans: list[str]

PLANNER = ( # TODO: Figure out how to integrate prompt_builder into this.
    "You are a chapter in a textbook planner. Given likely badly formatted input in the format of parsed slides/pdf/transcripts "
    "you will think deeply to decide things such as the format of the chapter, how many sections in the chapter and then "
    "you will return section_names and section_plans. A section_plan is a overview of what the chapter will contain. "
    "Remember that your goal is to produce a high quality plan of the chapter, where a LLM powered writer agent will turn that "
    "into longform text to be read, with the goal to educate. "
    "Attempt to stick as closely as possible to the provided context at all times. "
)

def generate_chapterplan(context: str, model="gpt-5"):
    return llm_tools.generate(PLANNER, context, model=model, structured_output=ChapterPlan)