# stack.py
# 역할: top / middle / base 이미지 3장을 하나의 vertical stack 이미지로 합성

from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "image"
OUT_DIR = IMAGE_DIR / "main"
OUT_DIR.mkdir(parents=True, exist_ok=True)

top_path = IMAGE_DIR / "top.png"
middle_path = IMAGE_DIR / "middle.png"
base_path = IMAGE_DIR / "base.png"

if not top_path.exists():
    raise FileNotFoundError("top.png not found")
if not middle_path.exists():
    raise FileNotFoundError("middle.png not found")
if not base_path.exists():
    raise FileNotFoundError("base.png not found")

top = Image.open(top_path).convert("RGB")
middle = Image.open(middle_path).convert("RGB")
base = Image.open(base_path).convert("RGB")

w, h = top.size

if middle.size != (w, h):
    middle = middle.resize((w, h), Image.BICUBIC)

if base.size != (w, h):
    base = base.resize((w, h), Image.BICUBIC)

stack = Image.new("RGB", (w, h * 3))

stack.paste(top, (0, 0))
stack.paste(middle, (0, h))
stack.paste(base, (0, h * 2))

output_path = OUT_DIR / "scent_stack.png"
stack.save(output_path)

print(f"✓ SCENT STACK SAVED → {output_path}")