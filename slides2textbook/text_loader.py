from pathlib import Path

def load_txt(path, encoding="utf-8"):
    with open(str(path)) as t:
        return t.read()