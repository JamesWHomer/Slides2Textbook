import logging
from pathlib import Path

from slides2textbook import cli
from slides2textbook import logconfig

logger = logging.getLogger(__name__)

def main(argv: list[str] | None = None) -> None:
    parser = cli.build_parser()
    args = parser.parse_args()
    logconfig.configure_logging(args.verbose, args.quiet, args.log_file)
    name = cli.resolve_output_name(args)

    try:
        run_pipeline(
            path=args.context_path,
            out_dir=args.out_dir,
            name=name,
            save_md = args.save_md,
            make_pdf=args.make_pdf,
            make_epub=args.make_epub,
            model=args.model,
            effort = args.effort,
            vision_model=args.vision_model or args.model,
            prev_chapters=args.prev_chapters,
            include_outline=args.include_outline,
        )
    except Exception:
        logger.exception("Unhandled error while running Slides2Textbook pipeline")
        raise SystemExit(1)

def run_pipeline(
    path: Path,
    out_dir: Path,
    name: str,
    save_md: bool,
    make_pdf: bool,
    make_epub: bool,
    model: str,
    effort: str,
    vision_model: str = "openai/gpt-5.4",
    prev_chapters: int = 0,
    include_outline: bool = False,
) -> None:
    from slides2textbook import context_loader, llm_tools, md_helper, prompt_builder as pb
    from slides2textbook.llm_classes import LLM_Response

    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting SlidesToTextbook, now loading context.")

    loaded_context: list[str] = context_loader.load_main_directory(path, vision_model=vision_model)

    if not loaded_context:
        logger.error("No context loaded, aborting program.")
        return

    instructions: str = context_loader.load_instructions(path)

    if instructions:
        logger.info(f"Textbook Instructions of length {len(instructions)} loaded.")
    else:
        logger.info("No textbook instructions loaded.")

    logger.info(f"Loaded textbook context, beginning to generate textbook of {len(loaded_context)} chapters.")

    token_count = llm_tools.TokenCount()
    system_prompt = pb.build_system_prompt()
    textbook: list[str] = []

    for idx, chapter_context in enumerate(loaded_context):
        path = out_dir / "chapters" / f"chapter-{str(idx + 1)}.md"
        if Path.is_file(path):
            logger.info(f"A chapter in {out_dir}/chapters with the name 'chapter-{str(idx + 1)}' already exists. Skipping LLM call and using existing chapter.")
            textbook.append(context_loader.load_textfile(path))
            continue
        logger.info("Generating chapter with context: " + chapter_context[:100].strip('\n') + "...")
        chapter_prompt = get_chapter_context(
            chapter_context,
            instructions,
            idx,
            textbook,
            name,
            prev_chapters=prev_chapters,
            include_outline=include_outline,
        )
        response: LLM_Response = llm_tools.generate(system_prompt, chapter_prompt, model_str=model, effort=effort)
        textbook.append(response.output_text)
        token_count.add(response.token_count)
        logger.info("Finished generating chapter: " + response.output_text[:100].strip('\n') + "...")
        md_helper.save_md(response.output_text, out_dir / "chapters", "chapter-" + str(idx + 1))

    logger.info(f"Converted slides to longform textbook.")
    logger.info(token_count)

    # Combine chapters into textbook string with spacing before each chapter
    textbook_str = "".join(f"\n\n{chapter}" for chapter in textbook)
    
    save_files(textbook_str, out_dir, name, save_md, make_pdf, make_epub)

def get_chapter_context(
    chapter_context: str,
    instructions: str,
    textbook_idx: int,
    textbook: list[str] | None,
    textbook_name: str,
    prev_chapters: int = 0,
    include_outline: bool = False,
) -> str:
    """Build the user prompt for one chapter.

    Args:
        prev_chapters: How many of the most recent previous chapters to include
            in full. 0 includes none; a negative value includes all of them.
        include_outline: Include the headings of previous chapters that are not
            fully in context, so the model knows what has already been covered.
    """
    from slides2textbook import md_helper

    parts: list[str] = []

    if instructions:
        parts.append("Whole Textbook Instructions:\n")
        parts.append(instructions)
        parts.append("\n\n")

    if textbook_idx > 0 and textbook:
        previous = textbook[:textbook_idx]
        if prev_chapters < 0:
            included = previous
        elif prev_chapters == 0:
            included = []
        else:
            included = previous[-prev_chapters:]
        outlined = previous[: len(previous) - len(included)]

        if include_outline and outlined:
            parts.append(
                "Outline of earlier chapters (headings only, full text not shown). "
                "Use this to know what has already been covered:\n\n"
            )
            outlines = [md_helper.extract_outline(chapter) for chapter in outlined]
            parts.append("\n\n".join(outline for outline in outlines if outline))
            parts.append("\n\n")

        if included:
            if len(included) == 1:
                parts.append("Previous chapter:\n")
            else:
                parts.append(f"Previous {len(included)} chapters:\n")
            parts.append("\n\n".join(included))
    else:
        parts.append(
            "You are now generating the first chapter of the textbook. "
            "Make sure to include the title of the book. (# Title)"
        )
        if textbook_name:
            parts.append(
                f"The provided title for the textbook is {textbook_name}, "
                "however you may modify or format this if you see fit. "
            )

    parts.append("\n\nCurrent chapter input context:\n\n")
    parts.append(chapter_context)

    return "".join(parts)

def save_files(textbook_str: str, out_dir: Path, name: str, save_md: bool = True, make_pdf: bool = True, make_epub: bool = True):
    """
    Function to simplify run_pipeline.
    """
    from slides2textbook import md_helper

    if save_md:
        md_helper.save_md(textbook_str, out_dir, name)
        logger.info(f"Saved markdown to {out_dir}/{name}")
    if make_pdf:
        md_helper.md_to_pdf(textbook_str, out_dir, name)
        logger.info(f"Saved PDF to {out_dir}/{name}")
    if make_epub:
        md_helper.md_to_epub(textbook_str, out_dir, name)
        logger.info(f"Saved EPUB to {out_dir}/{name}")
    if not save_md and not make_pdf:
        logger.warning("Nothing saved as both --no-md and --no-pdf flags were set. ")

if __name__ == "__main__":
    main()