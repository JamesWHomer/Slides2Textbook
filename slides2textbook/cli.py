import argparse
from pathlib import Path

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Slide2Textbook',
        description="Slide2Textbook allows you to convert pdf's and other context into high quality textbooks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-l", "--load-context", dest="context_path", required=True, type=existing_dir, help="The path to a directory that contains the context of the textbook (e.g. -l codingtextbook)")
    parser.add_argument("-o", "--out-dir", type=Path, default=Path("output"), help="Directory to place outputs")
    parser.add_argument("-n", "--name", help="Basename for outputs (defaults to PDF filename)")
    parser.add_argument("--no-md", dest="save_md", action="store_false", help="Skip saving the markdown file")
    parser.add_argument("--no-pdf", dest="make_pdf", action="store_false", help="Skip saving the pdf file")
    parser.add_argument("--no-epub", dest="make_epub", action="store_false", help="Skip saving the epub file")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (use -vv for more)")
    parser.add_argument("-q", "--quiet", action="count", default=0, help="Decrease verbosity (use -qq to silence info)")
    parser.add_argument("-m", "--model", type=str, default="gpt-5", help="Specify which model will be used to generate the textbook.")
    parser.add_argument("--log-file", type=Path, default=None, help="Optional path to write logs (in addition to stderr).")
    return parser

def existing_file(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"{p} does not exist or is not a file")
    return p

def existing_dir(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"{p} does not exist or is not a directory")
    return p

def resolve_output_name(args: argparse.Namespace) -> str:
    """Return output basename from -n or input context path name."""
    if args.name:
        return args.name
    context_path = getattr(args, "context_path", None)
    if context_path:
        if not isinstance(context_path, Path):
            context_path = Path(context_path)
        if context_path.is_file():
            return context_path.stem
        if context_path.is_dir():
            if context_path.name:
                return context_path.name
    return "textbook"