from pathlib import Path
from slides2textbook import pdf_decoder

def load_context(paths: list[Path]) -> str:
    context_dict = {}
    for file in paths:
        file.suffix
        match file.suffix:
            case ".pdf":
                context_dict[file.stem] = pdf_decoder.to_md(file)
            case ".txt":
                context_dict[file.stem] = load_textfile(file)
            case _: # TODO: There has **got** to be a better way to do this... Shit code, redo.
                # logger.exception("Unsupported filetype included in context") # TODO: logger here
                raise SystemExit(1)
    return context_formatter(context_dict)

def context_formatter(**contexts):
    context = ""
    for key, value in contexts.items():
        context += f"{key}:\n{value}\n\n"
    return context

def load_textfile(path: Path, encoding="utf-8") -> str:
    """ 
    Read and return the entire contexts of a text file. 
    """
    with open(str(path), 'r', encoding=encoding) as t:
        return t.read()