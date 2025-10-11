# The main orchestrator.
from slides2textbook import pdf_decoder
from slides2textbook import llm_tools
from slides2textbook import md_saver
from slides2textbook import md_to_pdf
from slides2textbook import prompt_builder as pb
from slides2textbook.agents import planner
from slides2textbook.agents import writer
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
            paths=args.context_paths,
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
    


def run_pipeline(paths: list[Path], out_dir: Path, name: str, save_md: bool, make_pdf: bool, agents: bool, model: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting SlidesToTextbook, now loading context.")

    context = context_loader.load_context(paths)
    
    logger.info("Loaded context, beginning to generate chapter.")

    input_tokens = output_tokens = 0

    if agents:
        inp, out, plan = planner.generate_chapterplan(context, model=model, effort="high")
        input_tokens += inp
        output_tokens += out
        logger.info("Finished plan: \n" + str(plan))
        chapter = ""
        for section_plan in plan.sections:
            logger.info("Generating section plan: " + section_plan.name)
            inp, out, section = writer.generate_section(context, chapter, section_plan, model=model, effort="high")
            chapter += "\n" + str(section)
            input_tokens += inp
            output_tokens += out
    else:
        SYSTEM_PROMPT = pb.build_system_prompt()
        inp, out, chapter = llm_tools.generate(SYSTEM_PROMPT, context, model=model)
        input_tokens += inp
        output_tokens += out

    logger.info(f"Converted slides to longform textbook. Total Input Tokens: {input_tokens}, Total Output Tokens: {output_tokens}")
    
    if save_md:
        md_saver.save_md(chapter, str(out_dir), name)
        logger.info(f"Saved markdown to {out_dir}/{name}")
    if (make_pdf):
        md_to_pdf.mdToPdf(chapter, str(out_dir), name)
        logger.info(f"Saved PDF to {out_dir}/{name}")
    if not save_md and not make_pdf:
        logger.warning("Nothing saved as both --no-md and --no-pdf flags were set. ")

if __name__ == "__main__":
    main()