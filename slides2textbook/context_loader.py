import logging
import os
from pathlib import Path

from openai.types import file_chunking_strategy
from slides2textbook import pdf_decoder

logger = logging.getLogger(__name__)

def load_main_directory(path: Path) -> list[str]:
    """
    Load all the subdirectories and their files as their respective chapter context. 
    Each chapter context is created based on the context held within each chapter directory in alphabetic order.
    """
    logger.info(f"Loading main directory at Path: {str(path)}")
    dirs = sorted((p for p in path.iterdir() if p.is_dir()), key=lambda p: p.name)

    if dirs:
        return [load_directory(chapter_context) for chapter_context in dirs]
        
    chapters = load_directory_chapters(path)
    if len(chapters) < 1:
        logger.error("No context loaded. Aborting program.")
    return chapters


def load_directory_chapters(path: Path) -> list[str]:
    """
    Load directory as textbook context where each set of files that share the same basename is considered a seperate chapter context.
    """
    files = sorted(
        (p for p in path.rglob("*") if p.is_file()), 
        key=lambda p: (p.relative_to(path).parent.as_posix(), p.name),
    )

    if not files:
        return []

    chapters: list[list[Path]] = []
    current: list[Path] = []

    for file in files:
        if current and file.stem != current[-1].stem:
            chapters.append(current)
            current = []
        current.append(file)
    
    if current:
        chapters.append(current)

    return [load_context(chapter) for chapter in chapters]

def load_directory(path: Path) -> str:
    """
    Load directory as chapter context, recursive inclusion of subdirectories, sorted by relative folder, then filename.
    """
    files = sorted(
        (p for p in path.rglob("*") if p.is_file()), 
        key=lambda p: (p.relative_to(path).parent.as_posix(), p.name),
    )

    return load_context(files)

def load_context(paths: list[Path] | Path) -> str:
    """ 
    Loads the list of paths and returns a combined LLM readable string.
    """

    if isinstance(paths, Path):
        paths = [paths]

    context_dict = {}
    common_path = Path(os.path.commonpath([str(p) for p in paths]))
    base_path = common_path.parent if common_path.is_file() else common_path
    for file in paths:
        file.suffix
        key = file.relative_to(base_path).as_posix()
        match file.suffix:
            case ".pdf":
                context_dict[key] = pdf_decoder.to_md(file)
            case ".txt" | ".md" | ".json" | ".html": # TODO: A lot more, if this is the approach we are taking.
                context_dict[key] = load_textfile(file)
            case _: # TODO: There has **got** to be a better way to do this... Shit code, redo.
                logger.error("Unsupported filetype included in context")
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