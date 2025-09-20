# The main orchestrator.
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

    print(args)

    name = args.name or args.pdf.stem

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
    


def run_pipeline(pdf: Path, txt: Path | None, out_dir: Path, name: str, save_md: bool, make_pdf: bool) -> None:
    print("Starting SlidesToTextbook, now loading context.")
    md = pdf_decoder.to_md("input\ISYS7.pdf")
    trans = text_loader.load_txt("input\ISYS7.txt")
    context = llm_tools.context_creator(markdown_file=md, transcript=trans)
    print("Loaded context, beginning to generate chapter.")
    chapter = llm_tools.to_chapter(context)
    print("Converted slides to longform textbook")
    md_saver.save_md(chapter, "output", "ISYS7")
    md_to_pdf.mdToPdf(chapter, "output", "ISYS7")
    print("Saved markdown file and pdf.")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Slides2Textbook',
        description="Allows you to convert pdf's and other context into high quality textbooks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--pdf", required=True, type=existing_file, help="Path to input slides PDF")
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