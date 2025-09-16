from pathlib import Path

def load_txt(path):
    txt_path = Path(path)
    with open(str(txt_path)) as t:
        return t.read()