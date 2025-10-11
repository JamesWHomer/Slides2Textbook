import argparse
from pathlib import Path

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Slide2Textbook',
        description="Slide2Textbook allows you to convert pdf's and other context into high quality textbooks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-l", "--load-context", dest="context_paths", nargs='+', type=existing_file, default=[], help="One or more files to preload into the context (e.g. -l notes/outline.txt slides/deck.pdf)")
    parser.add_argument("-o", "--out-dir", type=Path, default=Path("output"), help="Directory to place outputs")
    parser.add_argument("-n", "--name", help="Basename for outputs (defaults to PDF filename)")
    parser.add_argument("--no-md", dest="save_md", action="store_false", help="Skip saving the markdown file")
    parser.add_argument("--no-pdf", dest="make_pdf", action="store_false", help="Skip saving the pdf file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (use -vv for more)")
    parser.add_argument("-q", "--quiet", action="count", default=0, help="Decrease verbosity (use -qq to silence info)")
    parser.add_argument("-a", "--agents", dest="agents", action="store_true", help="Enable agent mode with a planner and writer, much more expensive.")
    parser.add_argument("-m", "--model", type=str, default="gpt-5", help="Specify which model will be used to generate the textbook.")
    parser.add_argument("--log-file", type=Path, default=None, help="Optional path to write logs (in addition to stderr).")
    return parser

def existing_file(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"{p} does not exist or is not a file")
    return p

def resolve_output_name(args: argparse.Namespace) -> str:
    if args.name:
        return args.name
    elif args.pdf:
        return args.pdf.stem
    elif args.txt:
        return args.txt.stem
    else:
        return "textbook"