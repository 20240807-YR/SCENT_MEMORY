# sd_generate.py
from pathlib import Path
import os
import json
import torch
from diffusers import StableDiffusionPipeline

from prompt_builder import load_perfume_json
from demo_weather import get_weather, weather_to_visual_context
from ollama_prompt import generate_all_prompts

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "image"
IMAGE_DIR.mkdir(exist_ok=True)

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
).to("cpu")

perfume = load_perfume_json()
weather = get_weather()
weather_context = weather_to_visual_context(weather)

ENV_NOTE_PROMPTS = os.environ.get("SCENT_NOTE_PROMPTS")
if ENV_NOTE_PROMPTS:
    NOTE_PROMPTS = json.loads(ENV_NOTE_PROMPTS)
else:
    NOTE_PROMPTS = generate_all_prompts()

def generate_note_image(note_type: str):
    visual_prompt = NOTE_PROMPTS[note_type]

    final_prompt = f"""
{visual_prompt}

Atmosphere modifier:
{weather_context}

Abstract, texture, motion, light, no objects, no text.
"""

    image = pipe(
        final_prompt,
        num_inference_steps=20
    ).images[0]

    output_path = IMAGE_DIR / f"{note_type}.png"
    image.save(output_path)
    print(f"✓ Generated {note_type}.png")

if __name__ == "__main__":
    generate_note_image("top")
    generate_note_image("middle")
    generate_note_image("base")