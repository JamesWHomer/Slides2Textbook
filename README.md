# Slides2Textbook

A simple python command line tool that uses LLM's to convert context (slides, lecture transcripts, notes, etc) into well formatted, focused and coherent textbooks.

Check out the Slides2Textbook [Github Project](https://github.com/users/JamesWHomer/projects/3/views/3) to track the development!

## Disclaimer

This project is **not** production ready. There will be bugs, issues and lack of support. Use at your own risk.

Note that Anthropic models are not currently supported.

## Guide

Ensure that python (3.10+ required) and git are installed on your PATH.

### Installation

Slides2Textbook can be installed quickly by running:

`pip install git+https://github.com/JamesWHomer/Slides2Textbook.git`

### Updating Slides2Textbook

`pip install --upgrade git+https://github.com/JamesWHomer/Slides2Textbook.git`

or for updating when there hasn't been a formal update:

`pip install --force-reinstall git+https://github.com/JamesWHomer/Slides2Textbook.git`

### Configure API credentials

API keys are stored and used on your system using something called "Environment Variables". You can set them however you please however if you are inexperienced with this, this is how:

1. Obtain and copy a valid API key from either the [OpenAI API](https://platform.openai.com/) or [Gemini API](https://ai.google.dev/gemini-api/docs).
2. Navigate to the Slides2Textbook directory (if you just following the Installation section you are already likely in the correct directory)
3. Set the Environment Variables:
  Use `OPENAI_API_KEY` for OpenAI. `GEMINI_API_KEY` for Google, `ANTHROPIC_API_KEY` for Anthropic.
   - macOS/Linux: `export PROVIDER_API_KEY="sk-...your_key_here..."` (temporary, only for current terminal)
   - Windows (Powershell): `$env:PROVIDER_API_KEY = "sk-...your_key_here..."` (temporary, only for current terminal)
   - Windows (cmd): `set PROVIDER_API_KEY=sk-...your_key_here...` (temporary, only for current terminal)
   - If Slides2Textbook is used with a `.env` file in the same directory it is run from, any api key environment variables will be loaded from there.
   - If your system supports setting environment variables in other ways, you can likely use that as an alternative. It is likely much more convenient to set environment variables permanently.

### Usage

Before running commands, use `cd <path to directory>` to navigate your terminal to the directory containing your input files.

- Run help: `slides2textbook -h`

Command synopsis (common options):

- `-l, --load PATH`: Path to the input directory that contains the files to be loaded.
- `-o, --out-dir PATH`: Output directory. Default: `output`.
- `-n, --name NAME`: Basename for outputs. Defaults to the input directory name; otherwise `textbook`.
- `--no-md`: Do not save the Markdown file into the output directory.
- `--no-pdf`: Do not generate and save the PDF file into the output directory.
- `--no-epub`: Do not generate and save the EPUB file into the output directory.
- `-v, --verbose`: Increase logging verbosity; repeat for more detail (e.g., `-vv`).
- `-q, --quiet`: Decrease logging verbosity; repeat to suppress more (e.g., `-qq`).
- `-m, --model`: Specify the API provider ('openai', 'gemini', or 'anthropic') and model name (e.g. 'gpt-5.4', 'gpt-4.1-mini') in the format of `<provider>/<model>`.
- `-e, --effort`: Specify the reasoning effort that the model uses. The model specific must support reasoning controls to be able to use this flag.
- `--vision-model`: Override the model used for image transcription (defaults to -m). Format: `<provider>/<model>`.
- `--log-file PATH`: Also write logs to the specified file.

Examples:

This is a basic example sufficient for 90% of usecases: `slides2textbook -l maths_textbook/input -o maths_textbook/output -n "Mathematics Textbook" -m openai/gpt-5.4 -e high`

Check out more examples on the [Github](https://github.com/JamesWHomer/Slides2Textbook/tree/main/examples).

## Context Loading

Note that context is loaded from the input directory. There are two ways of loading context:

1. **Folder Based**: Each folder (in natural sort order, similar to alphabetic however for example 1,2,3,...,10,11 instead of 1, 10, 11, ..., 2) is considered it's own chapter. All files/context within the subchapters are loaded individually. This is the recommended method.
2. **Name Based**: Files in the folder are loaded in natural order. Files sharing the same stem (filename without extension) are treated as members of the same chapter.

Supported input file formats:

- `.pdf`
- `.txt`
- `.md`
- `.json`
- `.html`
- `.png`
- `.jpg`
- `.jpeg`

## Metadata

One feature that you may find useful is textbook_instructions.txt. When a txt file of that name is included in the main directory, it is used as instruction and included in the context of each LLM call, ensuring any specific instructions are followed.

Slides2Textbook does not currently support metadata for textbooks.

## AI Policy

AI can be used for guidance, automatic code review and as a stack overflow replacement, however any code written must be handwritten by a human. I don't have any issues with AI development and AI could be used easily to speed up development 100x in the short term, however this risks the loss of the mental map of the codebase and the experience gained in the development of this project. Any contributions must be 100% written by a human, we don't need more technical debt. However this being said, note the automated pull request reviews, we are not luddites.
