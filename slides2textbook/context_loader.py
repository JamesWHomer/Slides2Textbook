from pathlib import Path
from slides2textbook import pdf_decoder

def load_context(paths: list[Path]) -> str:
    """ 
    Loads files directd by a list of paths and returns a combined LLM readable str.
    """
    context_dict = {}
    for file in paths:
        file.suffix
        match file.suffix:
            case ".pdf":
                context_dict[file.stem] = pdf_decoder.to_md(file)
            case ".txt" | ".md" | ".json" | ".html": # TODO: A lot more, if this is the approach we are taking.
                context_dict[file.stem] = load_textfile(file)
            case _: # TODO: There has **got** to be a better way to do this... Shit code, redo.
                # logger.exception("Unsupported filetype included in context") # TODO: logger here
                raise SystemExit(1)
    return context_formatter(context_dict)

def context_formatter(context_dict):
    """
    Converts a dictionary of key and file text pairs into a LLM readable format.
    """
    context = ""
    for key, value in context_dict.items():
        context += f"{key}:\n{value}\n\n"
    return context

def load_textfile(path: Path, encoding="utf-8") -> str:
    """ 
    Read and return the entire contexts of a text file. 
    """
    with open(str(path), 'r', encoding=encoding) as t:
        return t.read()