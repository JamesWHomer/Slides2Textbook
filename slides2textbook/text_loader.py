from pathlib import Path

def load_txt(path, encoding="utf-8"):
    with open(str(path), 'r', encoding=encoding) as t:
        return t.read()