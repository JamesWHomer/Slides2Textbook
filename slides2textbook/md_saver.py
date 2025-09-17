from pathlib import Path

def save_md(md, out_dir, name):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / f"{name}.md").write_text(md, encoding="utf-8")