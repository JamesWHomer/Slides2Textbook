# The main orchestrator.
from dataclasses import make_dataclass
from slides2textbook import pdf_decoder
from slides2textbook import llm_tools
from slides2textbook import md_saver
from slides2textbook import md_to_pdf
from slides2textbook import text_loader
from slides2textbook import prompt_builder as pb
from slides2textbook.agents import planner
from slides2textbook.agents import writer
import argparse
from pathlib import Path

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args()
    # TODO: configure logging

    if args.name:
        name = args.name
    elif args.pdf:
        name = args.pdf.stem
    elif args.txt:
        name = args.txt.stem
    else:
        name = "textbook"
        
    try:
        run_pipeline(
            pdf=args.pdf,
            txt=args.txt,
            out_dir=args.out_dir,
            name=name,
            save_md = args.save_md,
            make_pdf=args.make_pdf,
            agents=args.agents
        )
    except Exception as e:
        print("Error:", e)
        raise SystemExit(1)
    


def run_pipeline(pdf: Path | None, txt: Path | None, out_dir: Path, name: str, save_md: bool, make_pdf: bool, agents: bool) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Starting SlidesToTextbook, now loading context.")
    md = pdf_decoder.to_md(pdf) if pdf else ""
    trans = text_loader.load_txt(txt) if txt else ""
    context = llm_tools.context_creator(markdown_file=md, transcript=trans)

    print("Loaded context, beginning to generate chapter.")

    if agents:
        plan = planner.generate_chapterplan(context, model="gpt-5", effort="high")
        print("Finished plan: \n" + str(plan))
        chapter = ""
        for section_plan in plan.sections:
            print("Generating section plan: " + section_plan.name)
            chapter += "\n" + str(writer.generate_section(context, chapter, section_plan, model="gpt-5", effort="high"))
    else:
        SYSTEM_PROMPT = pb.build_system_prompt()
        chapter = llm_tools.generate(SYSTEM_PROMPT, context, model="gpt-5")

    print("Converted slides to longform textbook")
    
    if save_md:
        md_saver.save_md(chapter, str(out_dir), name)
        print(f"Saved markdown to {out_dir}/{name}")
    if (make_pdf):
        md_to_pdf.mdToPdf(chapter, str(out_dir), name)
        print(f"Saved PDF to {out_dir}/{name}")
    if not save_md and not make_pdf:
        print("Nothing saved as both --no-md and --no-pdf flags were set. ")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Slide2Textbook',
        description="Slide2Textbook allows you to convert pdf's and other context into high quality textbooks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--pdf", type=existing_file, help="Path to input slides PDF")
    parser.add_argument("--txt", type=existing_file, help="Path to input txt context")
    parser.add_argument("-o", "--out-dir", type=Path, default=Path("output"), help="Directory to place outputs")
    parser.add_argument("-n", "--name", help="Basename for outputs (defaults to PDF filename)")
    parser.add_argument("--no-md", dest="save_md", action="store_false", help="Skip saving the markdown file")
    parser.add_argument("--no-pdf", dest="make_pdf", action="store_false", help="Skip saving the pdf file")
    parser.add_argument("-v", "--verbose", action="count", default=1, help="Increase verbosity (-v, -vv)")
    parser.add_argument("-a", "--agents", dest="agents", action="store_true", help="Enable agent mode with a planner and writer, much more expensive.")
    return parser

def existing_file(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"{p} does not exist or is not a file")
    return p

if __name__ == "__main__":
    main()