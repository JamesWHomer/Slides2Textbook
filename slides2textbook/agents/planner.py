from pydantic import BaseModel
from slides2textbook import llm_tools


class SectionPlan(BaseModel):
    name: str
    plan_bulletpoints: list[str]

    def __str__(self) -> str:
        lines = [f"{self.name} {{ \n"]
        for point in self.plan_bulletpoints:
            lines.append(f"- {point}\n")
        lines.append("}\n")
        return "".join(lines)


class ChapterPlan(BaseModel):
    sections: list[SectionPlan]

    def __str__(self) -> str:
        return "".join(str(section) for section in self.sections)

PLANNER = ( # TODO: Figure out how to integrate prompt_builder into this.
    "You are a chapter in a textbook planner. Given likely badly formatted input in the format of parsed slides/pdf/transcripts "
    "you will think deeply to decide things such as the format of the chapter, how many sections in the chapter and then "
    "you will return section_names and section_plans. A section_plan is a overview of what the chapter will contain. "
    "Remember that your goal is to produce a high quality plan of the chapter, where a LLM powered writer agent will turn that "
    "into longform text to be read, with the goal to educate. "
    "Attempt to stick as closely as possible to the provided context at all times. "
    "Provide the format as short bulletpoints, however due not actually output - or newlines or unecessary whitespace as it will be added automatically. "
    "Assume that any bulletpoint not included will be left out of the textbook. "
    "Take a very minimal approach to the number of sections in the plan with as few as needed."
)

def generate_chapterplan(context: str, model="gpt-5", effort="high"):
    generation = llm_tools.generate(PLANNER, context, model=model, effort=effort, structured_output=ChapterPlan)
    return generation