import os
import base64
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

prompt = """
Abstract visual representing citrus fragrance notes.
Bright colors, light particles, fast diffusion.
Minimal composition.
No objects, no text.
Soft glow, airy feeling.
"""

result = client.images.generate(
    model="gpt-image-1",   # OpenAI 이미지 생성 모델
    prompt=prompt,
    size="1024x1024"
)

# base64 → bytes 변환
image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

with open("scent_stack_top.png", "wb") as f:
    f.write(image_bytes)

print("generated scent_stack_top.png")