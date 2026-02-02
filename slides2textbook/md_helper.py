"""
Module for saving and converting Markdown data.
"""

from pathlib import Path
from markdown_pdf import MarkdownPdf, Section
import pypandoc

def save_md(md: str, out_dir: Path, name: str) -> None:
    """
    Saves the provided markdown data to out_dir/name.md
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.md").write_text(md, encoding="utf-8")

def md_to_pdf(md: str, out_dir: Path, name: str) -> None:
    """
    Converts md string to a PDF using markdown-pdf and saves it to out_dir/name.pdf
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{name}.pdf"

    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(md))
    pdf.save(str(pdf_path))

def md_to_epub(md: str, out_dir: Path, name: str) -> None:
    """
    Converts md string to an EPUB using pandoc and saves it to out_dir/name.epub
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    epub_path = out_dir / f"{name}.epub"

    pypandoc.convert_text(
        md,
        "epub3",
        format="markdown+tex_math_single_backslash+tex_math_dollars",
        outputfile=str(epub_path),
        extra_args=[
            "--mathml",
        ],
    )