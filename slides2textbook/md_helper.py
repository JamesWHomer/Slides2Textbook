"""
Module for saving and converting Markdown data.
"""

import logging
import re
import tempfile
from pathlib import Path

import pypandoc
from markdown_pdf import MarkdownPdf, Section

logger = logging.getLogger(__name__)


_DISPLAY_MATH_LEADING_OPERATOR = re.compile(
    r"(?m)^(?P<indent>[ \t]*)(?P<opening>\\\[|\$\$)[ \t]*\r?\n"
    r"(?P=indent)(?P<operator>[+*-])[ \t]*\r?\n"
)


def _normalize_display_math(md: str) -> str:
    """Keeps leading math operators from being parsed as Markdown lists."""
    return _DISPLAY_MATH_LEADING_OPERATOR.sub(
        lambda match: (
            f"{match.group('indent')}{match.group('opening')}\n"
            f"{match.group('indent')}{match.group('operator')}"
        ),
        md,
    )


_ATX_HEADING = re.compile(r"^ {0,3}(?P<level>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")


def extract_outline(md: str, max_level: int = 6) -> str:
    """
    Extracts the Markdown ATX headings (up to max_level) from md, skipping
    headings inside fenced code blocks. Returns them joined by newlines.
    """
    headings: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in md.splitlines():
        stripped = line.strip()
        if in_fence:
            if stripped.startswith(fence_marker):
                in_fence = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = True
            fence_marker = stripped[:3]
            continue
        match = _ATX_HEADING.match(line)
        if match and len(match.group("level")) <= max_level:
            headings.append(f"{match.group('level')} {match.group('text')}")
    return "\n".join(headings)


def save_md(md: str, out_dir: Path, name: str) -> None:
    """
    Saves the provided markdown data to out_dir/name.md
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{name}.md").write_text(
        _normalize_display_math(md),
        encoding="utf-8",
    )

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
    md = _normalize_display_math(md)
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
    pdf.add_section(Section(_normalize_display_math(md)))
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
        _normalize_display_math(md),
        "epub3",
        format="markdown+tex_math_single_backslash+tex_math_dollars",
        outputfile=str(out_path),
        extra_args=extra_args,
    )
