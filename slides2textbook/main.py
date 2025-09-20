# The main orchestrator.
from slides2textbook import pdf_decoder
from slides2textbook import llm_tools
from slides2textbook import md_saver
from slides2textbook import md_to_pdf
from slides2textbook import text_loader

def main():
    print("Starting SlidesToTextbook, now loading context.")
    md = pdf_decoder.to_md("input\ISYS7.pdf")
    trans = text_loader.load_txt("input\ISYS7.txt")
    context = llm_tools.context_creator(markdown_file=md, transcript=trans)
    print("Loaded context, beginning to generate chapter.")
    chapter = llm_tools.to_chapter(context)
    print("Converted slides to longform textbook")
    md_saver.save_md(chapter, "output", "ISYS7")
    md_to_pdf.mdToPdf(chapter, "output", "ISYS7")
    print("Saved markdown file and pdf.")

if __name__ == "__main__":
    main()