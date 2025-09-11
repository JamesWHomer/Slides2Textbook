import os
import re
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Optional
from textwrap import wrap

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=OPENAI_API_KEY)

REASONING_EFFORT = "high"
MODEL = "o3"

SLIDES_DIR = "slides"
# OUTPUT_PDF = "textbook.pdf"
MAX_CHARS_PER_LINE = 100  # for PDF text wrapping

# Characters that commonly break latin-1 encoding mapped to ASCII equivalents
UNICODE_REPLACEMENTS = {
    "\u2013": "-",  # en dash
    "\u2014": "-",  # em dash
    "\u2018": "'",  # left single quote
    "\u2019": "'",  # right single quote
    "\u201c": '"',  # left double quote
    "\u201d": '"',  # right double quote
    "\u2026": "...",  # ellipsis
}


def sanitize_filename(filename: str) -> str:
    """Remove/replace characters that are invalid on most filesystems."""
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    sanitized = re.sub(r"\s+", "_", sanitized)
    return sanitized


def get_completion(system_prompt: str, user_prompt: str):
    """Get completion from OpenAI API (wrapper around simple call)."""
    params = {
        "model": MODEL,
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if MODEL.startswith("o"):
        params["reasoning"] = {"effort": REASONING_EFFORT}

    response = client.responses.create(**params)
    return response.output_text, {
        "prompt_tokens": response.usage.input_tokens,
        "completion_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
    }


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file using pdfplumber."""
    text_parts: List[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)


def make_ascii_safe(text: str) -> str:
    """Replace problematic unicode chars and strip those unsupported by latin-1."""
    for orig, repl in UNICODE_REPLACEMENTS.items():
        text = text.replace(orig, repl)

    # Normalize & drop remaining non-latin-1 chars
    import unicodedata

    normalized = unicodedata.normalize("NFKD", text)
    ascii_bytes = normalized.encode("latin-1", "ignore")
    return ascii_bytes.decode("latin-1")


def generate_chapter(slide_text: str, chapter_number: int, chapter_title: str, previous_chapter: Optional[str] = None):
    """Generate a textbook chapter using slide text as source."""
    system_prompt = (
        "You are an expert academic writer. Convert raw text extracted from OFFICIAL lecture slides into a clear, coherent textbook chapter in Markdown that maximises a reader's ability to excel in the INFO1111 Advanced Knowledge Exam (open-ended, insight-focused questions).\n\n"
        "Guidelines:\n"
        "• Retain every relevant term, definition, formula, code snippet, and diagram description that conveys the SUBJECT MATTER.\n"
        "• Expand terse bullet points into well-connected sentences and paragraphs so the chapter reads like flowing prose (lists only when strictly necessary).\n"
        "• Emphasise conceptual understanding, real-world significance, and the rationale behind ideas—so readers can justify, evaluate, and apply concepts as required by the exam.\n"
        "• Where appropriate, illustrate concepts with concise examples or scenarios drawn from the slide content to demonstrate application.\n"
        "• Omit administrative/logistical course details (assessment dates, lecture times, staff names) unless essential to understand the subject matter.\n"
        "• Organise material with clear hierarchical headings.\n"
        "• Write concisely in professional, straightforward prose—no quotes, puzzles, jokes, anecdotes, or filler. Maintain natural flow without verbosity.\n"
        "• Elaborate only to clarify existing slide content; do NOT invent new facts beyond the slides.\n"
        "• Avoid meta commentary and do NOT mention these guidelines or your role.\n"
    )

    user_prompt = (
        f"You are given the extracted text from a lecture slide deck. Use this content as the sole source to write Chapter {chapter_number}: {chapter_title}.\n\n"
        "RAW SLIDE CONTENT:\n" + slide_text + "\n\n"
        "Remember: Include all original information faithfully, structure it like a textbook chapter, and follow the above guidelines without referencing them explicitly.\n"
    )

    if previous_chapter:
        user_prompt += (
            "\nPREVIOUS CHAPTER (for continuity, do NOT repeat content):\n" + previous_chapter + "\n\n"
            "Ensure smooth narrative flow from the previous chapter to this one."
        )

    return get_completion(system_prompt, user_prompt)


def save_markdown(markdown_path: str, content: str):
    """Write the accumulated markdown to disk with UTF-8 encoding."""
    with open(markdown_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)
    print(f"Markdown updated -> {markdown_path}")


def main():
    print("=== SLIDES  →  TEXTBOOK GENERATOR ===\n")

    if not os.path.isdir(SLIDES_DIR):
        raise FileNotFoundError(f"Slides directory '{SLIDES_DIR}' not found.")

    slide_files = sorted(
        [f for f in os.listdir(SLIDES_DIR) if f.lower().endswith(".pdf")]
    )

    if not slide_files:
        raise FileNotFoundError("No PDF slides found in the 'slides' directory.")

    textbook_title = input("Enter textbook title: ").strip() or "Generated Textbook"
    print(f"\nProcessing {len(slide_files)} slide decks...\n")

    chapters: List[dict] = []
    total_tokens = 0
    previous_chapter_content = None
    markdown_content = f"# {textbook_title}\n\n"
    markdown_path = sanitize_filename(textbook_title) + ".md"

    for idx, filename in enumerate(slide_files, start=1):
        pdf_path = os.path.join(SLIDES_DIR, filename)
        chapter_title = os.path.splitext(filename)[0].replace("_", " ")
        print(f"Generating Chapter {idx}: {chapter_title} from {filename} ...")

        slide_text = extract_text_from_pdf(pdf_path)
        chapter_content, usage = generate_chapter(
            slide_text=slide_text,
            chapter_number=idx,
            chapter_title=chapter_title,
            previous_chapter=previous_chapter_content,
        )

        chapters.append({
            "number": idx,
            "title": chapter_title,
            "content": chapter_content,
        })

        previous_chapter_content = chapter_content
        total_tokens += usage["total_tokens"]
        print(f"    Tokens used this chapter: {usage['total_tokens']} | Cumulative: {total_tokens}")

        # Append to markdown and save progress continuously
        markdown_content += chapter_content + "\n\n"
        save_markdown(markdown_path, markdown_content)

    print("\nAll chapters processed.")
    print(f"Markdown textbook saved as: {markdown_path}")
    print(f"Total OpenAI tokens consumed: {total_tokens}\n")


if __name__ == "__main__":
    main() 