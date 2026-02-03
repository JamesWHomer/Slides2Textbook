# Slides2Textbook

## Disclaimer

This is **not** a production ready (not even close) piece of software. There will be many fatal bugs, many issues and generally a lack of support. Use at your own risk. 

## FAQ

Question: What is this?  
Answer: A simple experiment to turn unstructured context such as pdf's or transcripts into textbooks.

Question: What about images?  
Answer: I intend on eventually implementing images however we'll see eventually. I've found that often images in pdf's are really badly structured, I'm thinking about using the whole page of a slide as context, etc, however there is a lot to consider.

Question: What is your goal?  
Answer: I'm considering turning this into a server to eventually be used in a product, I'm thinking a simple website converter.

## Guide
Ensure that python (3.10+ recommended) and git are installed on your PATH.
### Installation
At the current stage in this project there is little that has been completed in the way of deployment so it should be run through commandline like a standard python package.
1. **Clone to local**: navigate to your chosen directory, open a terminal and run `git clone https://github.com/JamesWHomer/Slides2Textbook.git`, then navigate (`cd Slides2Textbook`) into that directory.
2. **Create venv**: Not specifically required but is best practice, create a python venv (Virtual Environment) with (macOS/Linux: `python3 -m venv .venv`) (Windows: `python3 -m venv .venv`)
3. **Activate venv**: (macOS/Linux: `source .venv/bin/activate`) (windows (powershell): `.\.venv\Scripts\Activate.ps1`) (Windows (cmd) `.venv\Scripts\activate.bat`)
4. **Install packages**: `pip install -r requirements.txt`

### Configure OpenAI credentials
1. Obtain and copy a valid [OpenAI key](https://platform.openai.com/)
2. Navigate to the Slides2Textbook directory (if you just following the Installation section you are already likely in the correct directory)
3. Store to local env:
   <!-- - macOS/Linux: `export OPENAI_API_KEY="sk-...your_key_here..."` (temporary)  !!! DOES NOT CURRENTLY FUNCTION !!!
   - Windows (Powershell): `$env:OPENAI_API_KEY = "sk-...your_key_here..."` (temporary) !!! DOES NOT CURRENTLY FUNCTION !!!
   - Windows (cmd): `set OPENAI_API_KEY=sk-...your_key_here...` (temporary) !!! DOES NOT CURRENTLY FUNCTION !!! --> 
   - Optional permanent .env file: Create a file named `.env` in the directory, containing `OPENAI_API_KEY=sk-...your_key_here...`. This will stay permanently unless deleted. 

### Usage

Slides2Textbook converts a slides PDF and/or a plain-text transcript into a long-form textbook chapter. It can save Markdown and/or a rendered PDF.

- Run help: `python -m slides2textbook -h`
- Typical run (PDF to Markdown + PDF): `python -m slides2textbook --pdf path/to/slides.pdf`

Command synopsis (common options):
- `-l, --load PATH`: Path to the input directory that contains the files to be loaded.
- `-o, --out-dir PATH`: Output directory. Default: `output`.
- `-n, --name NAME`: Basename for outputs. Defaults to the PDF filename (without extension); if no PDF, falls back to TXT filename; otherwise `textbook`.
- `--no-md`: Do not save the Markdown file.
- `--no-pdf`: Do not save the PDF file.
- `-v, --verbose`: Increase logging verbosity; repeat for more detail (e.g., `-vv`).
- `-q, --quiet`: Decrease logging verbosity; repeat to suppress more (e.g., `-qq`).
- `-m, --model`: Specify the model API name used (e.g., "gpt-5", "gpt-5-nano"). Note that it appears that currently only the gpt-5 family of models functions properly, this will be investigated later.
- `--log-file PATH`: Also write logs to the specified file.

Examples:
- Convert a PDF to both Markdown and PDF:  
  `python -m slides2textbook -l maths_textbook/input -o maths_textbook/output`
  TODO: More examples

Note that context is loaded from the specified main directory. There are two ways of loading context:
1. **Folder Based**: Each folder (in natural sort order, similar to alphabetic however for example 1,2,3,...,10,11 instead of 1, 10, 11, ..., 2) is considered it's own chapter. All files/context within the subchapters are loaded individually. This is the recommended method.
2. **Name Based**: Files in the folder are loaded in natural order. Files sharing the same stem (filename without extension) are treated as members of the same chapter.

## AI Policy
AI can be used for guidance, automatic code review and as a stack overflow replacement, however any code written must be handwritten by a human. I don't have any issues with AI development and AI could be used easily to speed up development 100x in the short term, however this risks the loss of the mental map of the codebase and the experience gained in the development of this project. Any contributions must be 100% written by a human.
