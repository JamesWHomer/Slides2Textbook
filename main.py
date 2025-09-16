# The main orchestrator.
import pdf_decoder
import llm_tools
import md_saver
import mdToPdf

def main():
    print("Starting SlidesToTextbook")
    md = pdf_decoder.to_md("06-LogicalDesignTheory-2025-v1.pdf")
    print("Converted slides to markdown file")
    chapter = llm_tools.to_chapter(context)
    print("Converted slides to longform textbook")
    md_saver.save_md(chapter, "output", "textbook")
    print("Saved markdown file of textbook")
    mdToPdf.mdToPdf(chapter, "output", "textbook")
    # print(chapter)

if __name__ == "__main__":
    main()