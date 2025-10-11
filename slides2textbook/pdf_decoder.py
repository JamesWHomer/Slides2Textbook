
from pathlib import Path
import pymupdf4llm as pf

def to_md(path):
    return pf.to_markdown(
        str(path),
        # write_images=False,
        # image_path=str(images_dir),
        # image_format="png",
    )
