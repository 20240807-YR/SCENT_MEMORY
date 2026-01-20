# sd_generate.py
from pathlib import Path
import os
import json
import torch
from diffusers import StableDiffusionPipeline
import argparse

from prompt_builder import load_perfume_json
from demo_weather import get_weather, weather_to_visual_context
from ollama_prompt import generate_visual_entities

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
    NOTE_PROMPTS_RAW = ENV_NOTE_PROMPTS
else:
    NOTE_PROMPTS_RAW = generate_visual_entities()
    os.environ["SCENT_NOTE_PROMPTS"] = NOTE_PROMPTS_RAW

NOTE_PROMPTS = {
    "top": NOTE_PROMPTS_RAW.split("TOP NOTE:")[1].split("MIDDLE NOTE:")[0].strip(),
    "middle": NOTE_PROMPTS_RAW.split("MIDDLE NOTE:")[1].split("BASE NOTE:")[0].strip(),
    "base": NOTE_PROMPTS_RAW.split("BASE NOTE:")[1].strip(),
}

def generate_note_image(note_type: str, out_path: Path | None = None):
    visual_prompt = NOTE_PROMPTS[note_type]

    final_prompt = f"""
{visual_prompt}

Atmospheric context:
{weather_context}

Abstract scent texture visualization,
no flowers, no petals, no plants, no botanical elements,
ethereal smoke clouds, ink diffusion in water,
soft color gradients, floating translucent particles,
amorphous shapes, no solid objects,
dreamlike, airy, scent-like presence,
minimal detail, no sharp edges,
high quality abstract texture, painterly diffusion
"""

    image = pipe(
        final_prompt,
        num_inference_steps=30,
        height=512,
        width=512
    ).images[0]

    output_path = out_path if out_path is not None else (IMAGE_DIR / f"{note_type}.png")
    image.save(output_path)
    print(f"✓ Generated {note_type}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--note", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    generate_note_image(
        args.note,
        Path(args.out)
    )