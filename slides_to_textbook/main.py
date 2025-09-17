# The main orchestrator.
from slides_to_textbook import pdf_decoder
from slides_to_textbook import llm_tools
from slides_to_textbook import md_saver
from slides_to_textbook import md_to_pdf
from slides_to_textbook import text_loader

def main():
    print("Starting SlidesToTextbook, now loading context.")
    md = pdf_decoder.to_md("input\L - week 7 - intro to Turing Machines.pdf")
    trans = text_loader.load_txt("input\Week 07 - Models of -transcript.txt")
    # context = llm_tools.context_creator(markdown_file=md, transcript=trans)
    context = llm_tools.context_creator(transcript=trans)
    # print(context)
    print("Loaded context, beginning to generate chapter.")
    chapter = llm_tools.to_chapter(context)
    print("Converted slides to longform textbook")
    md_saver.save_md(chapter, "output", "2922_lecture7_trans")
    md_to_pdf.mdToPdf(chapter, "output", "2922_lecture7_trans")
    print("Saved markdown file and pdf.")

if __name__ == "__main__":
    main()