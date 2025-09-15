from pathlib import Path
from markdown_pdf import MarkdownPdf, Section


def mdToPdf(md, out_dir, name):
    # Converts md string to a PDF using markdown-pdf and saves it to out_dir/name.pdf
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    pdf_path = out_path / f"{name}.pdf"

    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(md))
    pdf.save(str(pdf_path))