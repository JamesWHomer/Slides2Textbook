"""
Module for saving and converting Markdown data.
"""

import logging
import tempfile
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

_LATEX_PREAMBLE = r"""
\usepackage{enumitem}
\setlistdepth{9}

\renewlist{itemize}{itemize}{9}
\setlist[itemize,1]{label=\textbullet}
\setlist[itemize,2]{label=\textendash}
\setlist[itemize,3]{label=\textasteriskcentered}
\setlist[itemize,4]{label=\textperiodcentered}
\setlist[itemize,5]{label=\textbullet}
\setlist[itemize,6]{label=\textendash}
\setlist[itemize,7]{label=\textasteriskcentered}
\setlist[itemize,8]{label=\textperiodcentered}
\setlist[itemize,9]{label=\textbullet}

\renewlist{enumerate}{enumerate}{9}
\setlist[enumerate,1]{label=\arabic*.}
\setlist[enumerate,2]{label=\alph*.}
\setlist[enumerate,3]{label=\roman*.}
\setlist[enumerate,4]{label=\arabic*.}
\setlist[enumerate,5]{label=\alph*.}
\setlist[enumerate,6]{label=\roman*.}
\setlist[enumerate,7]{label=\arabic*.}
\setlist[enumerate,8]{label=\alph*.}
\setlist[enumerate,9]{label=\roman*.}
"""

def _md_to_pdf_pandoc(md: str, out_path: Path, toc: bool) -> None:
    """Converts md string to PDF via pandoc (requires a TeX engine on PATH)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".tex", delete=False, encoding="utf-8"
    ) as hdr:
        hdr.write(_LATEX_PREAMBLE)
        hdr_path = hdr.name

    extra_args = [
        "--pdf-engine=xelatex",
        "--variable=geometry:margin=1in",
        "--variable=fontsize=11pt",
        "--variable=linestretch=1.15",
        "--mathml",
        f"--include-in-header={hdr_path}",
    ]
    if toc:
        extra_args.append("--toc")

    try:
        pypandoc.convert_text(
            md,
            "pdf",
            format="markdown+tex_math_single_backslash+tex_math_dollars",
            outputfile=str(out_path),
            extra_args=extra_args,
        )
    finally:
        Path(hdr_path).unlink(missing_ok=True)

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