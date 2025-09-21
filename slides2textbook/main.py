# The main orchestrator.
from dataclasses import make_dataclass
from slides2textbook import pdf_decoder
from slides2textbook import llm_tools
from slides2textbook import md_saver
from slides2textbook import md_to_pdf
from slides2textbook import text_loader
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
        )
    except Exception as e:
        # TODO: Logging
        raise SystemExit(1)
    


def run_pipeline(pdf: Path | None, txt: Path | None, out_dir: Path, name: str, save_md: bool, make_pdf: bool) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Starting SlidesToTextbook, now loading context.")
    # TODO: modify to_md and load_txt to accept Path
    md = pdf_decoder.to_md(pdf) if pdf else ""
    trans = text_loader.load_txt(txt) if txt else ""
    context = llm_tools.context_creator(markdown_file=md, transcript=trans)

    print("Loaded context, beginning to generate chapter.")
    chapter = llm_tools.to_chapter(context)
    print("Converted slides to longform textbook")
    
    if save_md:
        md_saver.save_md(chapter, str(out_dir), name)
        print("Saved markdown to %s/%s", out_dir, name)
    if (make_pdf):
        md_to_pdf.mdToPdf(chapter, str(out_dir), name)
        print("Saved PDF to %s/%s", out_dir, name)
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
    return parser

def existing_file(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"{p} does not exist or is not a file")
    return p

if __name__ == "__main__":
    main()