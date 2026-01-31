# The main orchestrator.
from slides2textbook import pdf_decoder
from slides2textbook import llm_tools
from slides2textbook import md_saver
from slides2textbook import md_to_pdf
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
            model=args.model,
        )
    except Exception:
        logger.exception("Unhandled error while running Slides2Textbook pipeline")
        raise SystemExit(1)
    


def run_pipeline(path: Path, out_dir: Path, name: str, save_md: bool, make_pdf: bool, model: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting SlidesToTextbook, now loading context.")

    context: list[str] = context_loader.load_main_directory(path)

    logger.info(f"Loaded context of character length {len(context)}, beginning to generate textbook.")

    input_tokens = output_tokens = 0
    SYSTEM_PROMPT = pb.build_system_prompt()
    textbook: list[str] = []

    for idx, chapter_context in enumerate(context):
        if idx > 0:
            chapter_context = "Previous chapter: \n" + textbook[-1] + "\n\n" + "Current chapter input context: \n\n" + chapter_context
        inp, out, chapter = llm_tools.generate(SYSTEM_PROMPT, chapter_context, model=model)
        textbook.append(chapter)
        input_tokens += inp
        output_tokens += out
        logger.info("Finished generating chapter: " + chapter[:100])

    logger.info(f"Converted slides to longform textbook. Total Input Tokens: {input_tokens}, Total Output Tokens: {output_tokens}")

    textbook_str = ""
    for chapter in textbook:
        textbook_str += chapter
    
    if save_md:
        md_saver.save_md(textbook_str, str(out_dir), name)
        logger.info(f"Saved markdown to {out_dir}/{name}")
    if make_pdf:
        md_to_pdf.mdToPdf(textbook_str, str(out_dir), name)
        logger.info(f"Saved PDF to {out_dir}/{name}")
    if not save_md and not make_pdf:
        logger.warning("Nothing saved as both --no-md and --no-pdf flags were set. ")

if __name__ == "__main__":
    main()