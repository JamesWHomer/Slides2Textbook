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
        )
    except Exception:
        logger.exception("Unhandled error while running Slides2Textbook pipeline")
        raise SystemExit(1)
    


def run_pipeline(path: Path, out_dir: Path, name: str, save_md: bool, make_pdf: bool, make_epub: bool, model: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting SlidesToTextbook, now loading context.")

    context: list[str] = context_loader.load_main_directory(path)

    if not context:
        logger.error("No context loaded, aborting program.")
        return

    instructions: str = context_loader.load_instructions(path)

    if instructions:
        logger.info(f"Textbook Instructions of length {len(instructions)} loaded.")
    else:
        logger.info(f"No textbook instructions loaded.")

    logger.info(f"Loaded textbook context, beginning to generate textbook of {len(context)} chapters.")

    input_tokens = output_tokens = 0
    SYSTEM_PROMPT = pb.build_system_prompt()
    textbook: list[str] = []

    final_context: str = ""

    for idx, chapter_context in enumerate(context):
        if instructions:
            final_context = "Whole Textbook Instructions: \n" + instructions + "\n\n"
        else:
            final_context = ""
        if idx > 0:
            final_context += "Previous chapter: \n" + textbook[-1] 
        else:
            final_context += "You are now generating the first chapter of the textbook. Make sure to include the title of the book. "
            if name:
                final_context += f"The provided name for the textbook is {name}, however you may modify or format this if you see fit. "

        final_context += "\n\n" + "Current chapter input context: \n\n" + chapter_context
            
        inp, out, chapter = llm_tools.generate(SYSTEM_PROMPT, final_context, model=model)
        textbook.append(chapter)
        input_tokens += inp
        output_tokens += out
        logger.info("Finished generating chapter: " + chapter[:100].strip('\n') + "...")

    logger.info(f"Converted slides to longform textbook. Total Input Tokens: {input_tokens}, Total Output Tokens: {output_tokens}")

    textbook_str = ""
    for chapter in textbook:
        textbook_str += chapter
    
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