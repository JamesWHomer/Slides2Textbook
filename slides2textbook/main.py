# The main orchestrator.
from slides2textbook import pdf_decoder
from slides2textbook import llm_tools
from slides2textbook import md_saver
from slides2textbook import md_to_pdf
from slides2textbook import text_loader
from slides2textbook import prompt_builder as pb
from slides2textbook.agents import planner
from slides2textbook.agents import writer
from slides2textbook import cli
import logging
import argparse
from pathlib import Path

logger = logging.getLogger(__name__)

def main(argv: list[str] | None = None) -> None:
    parser = cli.build_parser()
    args = parser.parse_args()
    configure_logging(args.verbose, args.quiet, args.log_file)
    name = cli.resolve_output_name(args)

    try:
        run_pipeline(
            pdf=args.pdf,
            txt=args.txt,
            out_dir=args.out_dir,
            name=name,
            save_md = args.save_md,
            make_pdf=args.make_pdf,
            agents=args.agents,
            model=args.model,
        )
    except Exception:
        logger.exception("Unhandled error while running Slides2Textbook pipeline")
        raise SystemExit(1)
    


def run_pipeline(pdf: Path | None, txt: Path | None, out_dir: Path, name: str, save_md: bool, make_pdf: bool, agents: bool, model: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting SlidesToTextbook, now loading context.")
    md = pdf_decoder.to_md(pdf) if pdf else ""
    trans = text_loader.load_txt(txt) if txt else ""
    context = llm_tools.context_creator(markdown_file=md, transcript=trans)

    logger.info("Loaded context, beginning to generate chapter.")

    if agents:
        plan = planner.generate_chapterplan(context, model=model, effort="high")
        logger.info("Finished plan: \n" + str(plan))
        chapter = ""
        for section_plan in plan.sections:
            logger.info("Generating section plan: " + section_plan.name)
            chapter += "\n" + str(writer.generate_section(context, chapter, section_plan, model=model, effort="high"))
    else:
        SYSTEM_PROMPT = pb.build_system_prompt()
        chapter = llm_tools.generate(SYSTEM_PROMPT, context, model=model)

    logger.info("Converted slides to longform textbook")
    
    if save_md:
        md_saver.save_md(chapter, str(out_dir), name)
        logger.info(f"Saved markdown to {out_dir}/{name}")
    if (make_pdf):
        md_to_pdf.mdToPdf(chapter, str(out_dir), name)
        logger.info(f"Saved PDF to {out_dir}/{name}")
    if not save_md and not make_pdf:
        logger.warning("Nothing saved as both --no-md and --no-pdf flags were set. ")

def configure_logging(verbosity: int, quietness: int, log_file: Path | None) -> None:
    base_level = logging.INFO
    level = base_level - (verbosity * 10) + (quietness * 10)
    level = min(max(level, logging.DEBUG), logging.CRITICAL)
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        handlers=handlers,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

if __name__ == "__main__":
    main()