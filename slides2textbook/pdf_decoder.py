
from pathlib import Path
import pymupdf4llm as pf

# pdf_path = Path("06-LogicalDesignTheory-2025-v1.pdf")

# # choose where outputs should go (one folder per PDF is neat)
# out_dir = Path("outputs") / pdf_path.stem
# images_dir = out_dir / "images"
# images_dir.mkdir(parents=True, exist_ok=True)

# md = pf.to_markdown(
#     str(pdf_path),
#     write_images=False,            # extract images / vector graphics
#     image_path=str(images_dir),   # save images here
#     image_format="png",           # or "jpg" etc. (optional)
# )

# # write the markdown next to the images
# (out_dir / f"{pdf_path.stem}.md").write_text(md, encoding="utf-8")
# print(f"Saved Markdown to {out_dir} and images to {images_dir}")

def to_md(path):
    pdf_path = Path(path)
    return pf.to_markdown(
        str(pdf_path),
        # write_images=False,
        # image_path=str(images_dir),
        # image_format="png",
    )
