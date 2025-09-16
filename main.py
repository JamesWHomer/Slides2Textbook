# The main orchestrator.
from pydoc import text
import pdf_decoder
import llm_tools
import md_saver
import mdToPdf
import text_loader

def main():
    print("Starting SlidesToTextbook")
    md = pdf_decoder.to_md("06-LogicalDesignTheory-2025-v1.pdf")
    trans = text_loader.load_txt("Week 06 - Data and I-transcript.txt")
    context = llm_tools.context_creator(markdown_file=md, transcript=trans)
    print(context)
    print("Converted slides to markdown file")
    chapter = llm_tools.to_chapter(context)
    print("Converted slides to longform textbook")
    md_saver.save_md(chapter, "output", "textbook_with_speech")
    print("Saved markdown file of textbook")
    mdToPdf.mdToPdf(chapter, "output", "textbook_with_speech")
    print(chapter)

if __name__ == "__main__":
    main()