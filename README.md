# Slides2Textbook

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
   - macOS/Linux: `export OPENAI_API_KEY="sk-...your_key_here..."` (temporary)
   - Windows (Powershell): `$env:OPENAI_API_KEY = "sk-...your_key_here..."` (temporary)
   - Windows (cmd): `set OPENAI_API_KEY=sk-...your_key_here...` (temporary)
   - Optional permanent .env file: Create a file named `env` containing `OPENAI_API_KEY=sk-...your_key_here...`. This will stay permanently unless deleted. 

### Usage

Slides2Textbook converts a slides PDF and/or a plain-text transcript into a long-form textbook chapter. It can save Markdown and/or a rendered PDF.

- Run help: `python -m slides2textbook -h`
- Typical run (PDF to Markdown + PDF): `python -m slides2textbook --pdf path/to/slides.pdf`

Command synopsis (common options):
- `--pdf PATH`: Path to the input slides PDF (optional).
- `--txt PATH`: Path to a plain-text transcript or supplemental context (optional).
- `-o, --out-dir PATH`: Output directory. Default: `output`.
- `-n, --name NAME`: Basename for outputs. Defaults to the PDF filename (without extension); if no PDF, falls back to TXT filename; otherwise `textbook`.
- `--no-md`: Do not save the Markdown file.
- `--no-pdf`: Do not save the PDF file.
- `-v, --verbose`: Increase logging verbosity; repeat for more detail (e.g., `-vv`).
- `-q, --quiet`: Decrease logging verbosity; repeat to suppress more (e.g., `-qq`).
- `-a, --agents`: Enable planner/writer agent mode for higher-quality structured output (slower and more expensive).
- `--log-file PATH`: Also write logs to the specified file.

Examples:
- Convert a PDF to both Markdown and PDF:  
  `python -m slides2textbook --pdf slides/lecture1.pdf`
- Combine slides and transcript as context:  
  `python -m slides2textbook --pdf slides/lecture1.pdf --txt transcripts/lecture1.txt`
- Transcript-only to textbook:  
  `python -m slides2textbook --txt transcripts/lecture1.txt`
- Custom output directory and name:  
  `python -m slides2textbook --pdf slides/lecture1.pdf -o out/chapters -n intro-to-ml`
- Save only Markdown:  
  `python -m slides2textbook --pdf slides/lecture1.pdf --no-pdf`
- Save only PDF:  
  `python -m slides2textbook --pdf slides/lecture1.pdf --no-md`
- Agent mode (planner + writer):  
  `python -m slides2textbook --pdf slides/lecture1.pdf -a`
- More logs and write to file:  
  `python -m slides2textbook --pdf slides/lecture1.pdf -vv --log-file logs/run.log`
