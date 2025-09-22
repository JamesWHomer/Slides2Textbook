# The purpose of this is to eventually enable a way for users to modify what strings get included in the system prompt.

def get_system(idx: list[int]):
    return bullet_prompt_builder([get_promp_string(id) for id in idx])

def bullet_prompt_builder(prompts: list[str]) -> str:
    prompt = ""
    for s in prompts:
        prompt += f" - {s}\n"
    return prompt

def get_promp_string(idx: int) -> str:
    match idx:
        case 0:
            return ("You are a textbook chapter creator. Given a possibly badly structured markdown file likely created from pdf's/slides "
    "and missing information such as images, you will attempt to the best of your ability to create a high quality textbook chapter "
    "of the slides/notes in the markdown file provided, aiming to best educate the reader.")
        case 1:
            return "Base the textbook heavily off of the slides, do not miss any information or go too off topic from the textbook unless necessary."
        case 2:
            return "Respond in markdown format and assume that your response will be included in the chapter, so do not respond with anything but the textbook."
        case 3:
            return "Do not include unecessary artifacts from the previous format such as page numbers or repeated information such as headers."
        case 4:
            return "Do not include extra features such as exercises unless they are explicitely shown in the slides. Remember your tasks is to create a chapter based on slides, not a chapter itself."
        case 5:
            return "Note that a transcript will also possibly be attached from any lecture using that slide. Use the information to augment and determine what other information to include."
        case 6:
            return "Note that you will not able to see any images or create any images."
        case 7:
            return "The textbook chapter should be considered standalone."
        case 8:
            return "Do not start with a preamble, go into the textbook chapter immediately."