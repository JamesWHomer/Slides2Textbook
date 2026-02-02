# The main orchestrator.
from slides2textbook import pdf_decoder
from slides2textbook import llm_tools
from slides2textbook import md_helper
from slides2textbook import prompt_builder as pb
from slides2textbook import cli
from slides2textbook import logconfig
from slides2textbook import context_loader
import logging
from pathlib import Path

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
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting SlidesToTextbook, now loading context.")

    loaded_context: list[str] = context_loader.load_main_directory(path)

    if not loaded_context:
        logger.error("No context loaded, aborting program.")
        return

    instructions: str = context_loader.load_instructions(path)

    if instructions:
        logger.info(f"Textbook Instructions of length {len(instructions)} loaded.")
    else:
        logger.info("No textbook instructions loaded.")

    logger.info(f"Loaded textbook context, beginning to generate textbook of {len(loaded_context)} chapters.")

    input_tokens = output_tokens = 0
    system_prompt = pb.build_system_prompt()
    textbook: list[str] = []

    for idx, chapter_context in enumerate(loaded_context):
        chapter_prompt = get_chapter_context(
            chapter_context,
            instructions,
            idx,
            textbook,
            name,
        )
        inp, out, chapter = llm_tools.generate(system_prompt, chapter_prompt, model=model, effort=effort)
        textbook.append(chapter)
        input_tokens += inp
        output_tokens += out
        logger.info("Finished generating chapter: " + chapter[:100].strip('\n') + "...")

    logger.info(f"Converted slides to longform textbook. Total Input Tokens: {input_tokens}, Total Output Tokens: {output_tokens}")

    # Combine chapters into textbook string
    textbook_str = "".join(textbook)
    
    save_files(textbook_str, out_dir, name, save_md, make_pdf, make_epub)

def get_chapter_context(
    chapter_context: str,
    instructions: str,
    textbook_idx: int,
    textbook: list[str] | None,
    textbook_name: str,
) -> str:
    parts: list[str] = []

    if instructions:
        parts.append("Whole Textbook Instructions:\n")
        parts.append(instructions)
        parts.append("\n\n")

    if textbook_idx > 0 and textbook:
        parts.append("Previous chapter:\n")
        parts.append(textbook[textbook_idx - 1])
    else:
        parts.append(
            "You are now generating the first chapter of the textbook. "
            "Make sure to include the title of the book. "
        )
        if textbook_name:
            parts.append(
                f"The provided name for the textbook is {textbook_name}, "
                "however you may modify or format this if you see fit. "
            )

    parts.append("\n\nCurrent chapter input context:\n\n")
    parts.append(chapter_context)

    return "".join(parts)

def save_files(textbook_str: str, out_dir: Path, name: str, save_md: bool = True, make_pdf: bool = True, make_epub: bool = True):
    """
    Function to simplify run_pipeline.
    """
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