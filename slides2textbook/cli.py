import argparse
from pathlib import Path

def resolve_output_name(args: argparse.Namespace) -> str:
    if args.name:
        return args.name
    elif args.pdf:
        return args.pdf.stem
    elif args.txt:
        return args.txt.stem
    else:
        return "textbook"