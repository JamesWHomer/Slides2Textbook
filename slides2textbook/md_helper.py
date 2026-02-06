"""
Module for saving and converting Markdown data.
"""

import logging
from pathlib import Path

import pypandoc
from markdown_pdf import MarkdownPdf, Section

logger = logging.getLogger(__name__)

def save_md(md: str, out_dir: Path, name: str) -> None:
    """
    Saves the provided markdown data to out_dir/name.md
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.md").write_text(md, encoding="utf-8")

def _md_to_pdf_pandoc(md: str, out_path: Path, toc: bool) -> None:
    """Converts md string to PDF via pandoc (requires a TeX engine on PATH)."""
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

def _md_to_pdf_fallback(md: str, out_path: Path, toc: bool) -> None:
    """Converts md string to PDF via markdown-pdf (no TeX required)."""
    toc_level = 2 if toc else 0
    pdf = MarkdownPdf(toc_level=toc_level, optimize=True)
    pdf.add_section(Section(md))
    pdf.save(str(out_path))

def md_to_pdf(md: str, out_dir: Path, name: str, toc: bool = False) -> None:
    """
    Converts md string to a PDF and saves it to out_dir/name.pdf.
    Attempts high-quality export via pandoc + LaTeX first; if a TeX engine
    is not available, falls back to the markdown-pdf library.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}.pdf"

    try:
        _md_to_pdf_pandoc(md, out_path, toc)
    except (OSError, RuntimeError) as exc:
        logger.warning(
            "pandoc PDF export failed (%s). Falling back to markdown-pdf. "
            "For higher-quality PDFs, install a TeX engine "
            "(e.g. TeX Live, MiKTeX, or Tectonic).",
            exc,
        )
        _md_to_pdf_fallback(md, out_path, toc)

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