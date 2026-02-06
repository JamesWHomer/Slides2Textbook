"""
Module for saving and converting Markdown data.
"""

from pathlib import Path
import pypandoc

def save_md(md: str, out_dir: Path, name: str) -> None:
    """
    Saves the provided markdown data to out_dir/name.md
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.md").write_text(md, encoding="utf-8")

def md_to_pdf(md: str, out_dir: Path, name: str, toc: bool = False) -> None:
    """
    Converts md string to a PDF using pandoc and saves it to out_dir/name.pdf
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}.pdf"

    extra_args = [
        "--variable=geometry:margin=1in",
        "--variable=fontsize=11pt",
        "--variable=linestretch=1.15",
        "--mathml",
    ]
    if toc:
        extra_args.append("--toc")

    pypandoc.convert_text(
        md,
        "pdf",
        format="markdown+tex_math_single_backslash+tex_math_dollars",
        outputfile=str(out_path),
        extra_args=extra_args,
    )

def md_to_epub(md: str, out_dir: Path, name: str, toc: bool = False) -> None:
    """
    Converts md string to an EPUB using pandoc and saves it to out_dir/name.epub
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}.epub"

    extra_args = [
        "--mathml",
    ]
    if toc:
        extra_args.append("--toc")

    pypandoc.convert_text(
        md,
        "epub3",
        format="markdown+tex_math_single_backslash+tex_math_dollars",
        outputfile=str(out_path),
        extra_args=extra_args,
    )