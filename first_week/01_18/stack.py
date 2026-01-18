from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "image"
OUT_DIR = IMAGE_DIR / "main"
OUT_DIR.mkdir(parents=True, exist_ok=True)

top = Image.open(IMAGE_DIR / "top.png")
middle = Image.open(IMAGE_DIR / "middle.png")
base = Image.open(IMAGE_DIR / "base.png")

w, h = top.size
stack = Image.new("RGB", (w, h * 3))

stack.paste(top, (0, 0))
stack.paste(middle, (0, h))
stack.paste(base, (0, h * 2))

stack.save(OUT_DIR / "scent_stack.png")