# Slides2Textbook

## Guide
Ensure that python (3.10+ recommended) and git are installed on your PATH.
### Installation
At the current stage in this project there is little that has been completed in the way of deployment so it should be run through commandline like a standard python package.
1. **Clone to local**: navigate to your chosen directory, open a terminal and run `git clone https://github.com/JamesWHomer/Slides2Textbook.git`, then navigate (`cd Slides2Textbook`) into that directory.
2. **Create venv**: Not specifically required but is best practice, create a python venv (Virtual Environment) with (macOS/Linux: `python3 -m venv .venv`) (windows: `python3 -m venv .venv`)
3. **Activate venv**: (macOS/Linux: `source .venv/bin/activate`) (windows (powershell): `.\.venv\Scripts\Activate.ps1`) (windows (cmd) `.venv\Scripts\activate.bat`)
4. **Install packages**: `pip install -r requirements.txt`

## FAQ

Question: What is this?  
Answer: A simple experiment to turn unstructured context such as pdf's or transcripts into textbooks.

Question: What about images?  
Answer: I intend on eventually implementing images however we'll see eventually. I've found that often images in pdf's are really badly structured, I'm thinking about using the whole page of a slide as context, etc, however there is a lot to consider.

Question: What is your goal?  
Answer: I'm considering turning this into a server to eventually be used in a product, I'm thinking a simple website converter.
