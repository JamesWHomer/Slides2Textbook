#!/usr/bin/env python3
"""
Simple PDF Converter for Markdown Files
=======================================
Edit the MARKDOWN_FILE variable below to specify which file to convert.
"""

# Default markdown file (used only if none provided via CLI)
DEFAULT_MARKDOWN_FILE = "INFO1111_Exam_Textbook_Prep.md"

import pypandoc
import os
import sys  # For reading command-line arguments

# Choose PDF engine (using xelatex by default for reliable margin control)
PDF_ENGINE = "xelatex"

# Set desired margin in millimeters (typical ~20 mm ≈ 0.8")
MARGIN_MM = 20

def create_margin_css(margin_mm: int) -> str:
    """Create a temporary CSS file that sets the @page margin."""
    css_content = f"@page {{ margin: {margin_mm}mm; }}\nbody {{ margin: 0; }}"
    css_file = "temp_margin.css"
    with open(css_file, "w", encoding="utf-8") as f:
        f.write(css_content)
    return css_file

def convert_markdown_to_pdf(markdown_file):
    """Convert markdown file to PDF"""
    
    # Check if input file exists
    if not os.path.exists(markdown_file):
        print(f"Error: File '{markdown_file}' not found!")
        return None
    
    # Generate output filename
    pdf_filename = markdown_file.replace('.md', '.pdf')
    
    print(f"Converting '{markdown_file}' to PDF...")
    print(f"Using PDF engine: {PDF_ENGINE}")
    
    try:
        extra_args = [f'--pdf-engine={PDF_ENGINE}']

        # If using a LaTeX-based engine, leverage the geometry package for margins
        if PDF_ENGINE.lower() in {"xelatex", "lualatex", "pdflatex"}:
            # Pandoc passes variables to LaTeX templates with -V
            # geometry:margin accepts values like 0cm; convert mm → cm
            margin_cm = MARGIN_MM / 10
            extra_args += ["-V", f"geometry:margin={margin_cm}cm"]
            print(f"Using LaTeX margin: {margin_cm}cm")
        else:
            # For CSS-aware engines (e.g., weasyprint), create a temp CSS file
            css_file = create_margin_css(MARGIN_MM)
            extra_args.append(f"--css={css_file}")
            print(f"Using CSS margin: {MARGIN_MM}mm")

        print(f"Pandoc args: {extra_args}")
        print("Starting conversion...")

        # Perform conversion
        result = pypandoc.convert_file(
            markdown_file,
            'pdf',
            outputfile=pdf_filename,
            extra_args=extra_args
        )
        
        print("Conversion command completed")

        # Clean up any temp CSS file that may have been created
        try:
            if 'css_file' in locals() and os.path.exists(css_file):
                os.remove(css_file)
        except OSError:
            pass
        
        # Check if PDF was created
        if os.path.exists(pdf_filename):
            size = os.path.getsize(pdf_filename)
            print(f"Success! PDF created: {pdf_filename} ({size:,} bytes)")
            return pdf_filename
        else:
            print("Error: PDF file was not created")
            return None
            
    except Exception as e:
        print(f"Conversion failed: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return None

# ---------------- EPUB Conversion ----------------

def convert_markdown_to_epub(markdown_file):
    """Convert markdown file to EPUB"""

    # Check if input file exists
    if not os.path.exists(markdown_file):
        print(f"Error: File '{markdown_file}' not found!")
        return None

    # Generate output filename
    epub_filename = markdown_file.replace('.md', '.epub')

    print(f"Converting '{markdown_file}' to EPUB...")

    try:
        extra_args = []  # No special args required for basic EPUB output

        print(f"Pandoc args: {extra_args}")
        print("Starting conversion...")

        # Perform conversion
        result = pypandoc.convert_file(
            markdown_file,
            'epub',
            outputfile=epub_filename,
            extra_args=extra_args
        )

        print("Conversion command completed")

        # Check if EPUB was created
        if os.path.exists(epub_filename):
            size = os.path.getsize(epub_filename)
            print(f"Success! EPUB created: {epub_filename} ({size:,} bytes)")
            return epub_filename
        else:
            print("Error: EPUB file was not created")
            return None

    except Exception as e:
        print(f"Conversion failed: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return None

# -------------------- MAIN -----------------------

def main():
    print("=== MARKDOWN CONVERTER ===\n")

    # ---------------- CLI Parsing ----------------
    # Usage:
    #   python pdf_converter.py <markdown_file> [<output_format>]
    #   <output_format> defaults to 'pdf' if omitted (choices: pdf | epub)

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python pdf_converter.py <markdown_file> [<output_format>]")
        print("       <output_format>: pdf | epub  (default: pdf)")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_format = sys.argv[2].lower() if len(sys.argv) == 3 else 'pdf'

    if output_format == 'pdf':
        result = convert_markdown_to_pdf(markdown_file)
    elif output_format == 'epub':
        result = convert_markdown_to_epub(markdown_file)
    else:
        print(f"Error: Unsupported format '{output_format}'. Use 'pdf' or 'epub'.")
        sys.exit(1)

    if result:
        print(f"\nConversion completed: {result}")
    else:
        print("\nConversion failed.")

if __name__ == "__main__":
    main() 