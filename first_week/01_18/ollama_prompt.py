import os
# ollama_prompt.py

import subprocess
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
PERFUME_JSON = BASE_DIR / "lazy_sunday_morning.json"


def load_perfume_notes():
    with open(PERFUME_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["notes"]


def build_prompt(notes, weather_context=None):
    weather_block = ""
    if weather_context:
        weather_block = f"\nWeather context:\n{weather_context}\n"

    return f"""
You are a system that writes short, abstract visual prompts for Stable Diffusion image generation.

STRICT RULES:
- Output plain text only
- No JSON
- No markdown
- No explanation
- No titles
- Avoid photorealistic language
- Background should be soft and simple (no solid background color)

You must generate THREE separate prompts, one for each perfume note layer.
Each prompt should be 1–2 lines max and abstract flower-style.

Output format (MUST FOLLOW EXACTLY):

TOP NOTE:
(one short abstract flower-style image prompt)

MIDDLE NOTE:
(one short abstract flower-style image prompt)

BASE NOTE:
(one short abstract flower-style image prompt)

Perfume notes:
{json.dumps(notes, ensure_ascii=False, indent=2)}
{weather_block}

Example (FORMAT ONLY):

TOP NOTE:
A light abstract citrus blossom cluster, pale yellow tones, airy, floating, soft glow, isolated, soft background, no solid background color

MIDDLE NOTE:
A gentle lavender flower form, pastel purple tones, calm, smooth diffusion, dreamy, isolated, soft background, no solid background color

BASE NOTE:
A deep woody floral abstraction, muted brown and cream tones, dense, grounded, slow presence, isolated, soft background, no solid background color
"""


def generate_visual_entities(weather_context=None):
    notes = load_perfume_notes()
    prompt = build_prompt(notes, weather_context)

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    output = result.stdout.strip()

    return output


if __name__ == "__main__":
    ENV_NOTE_PROMPTS = os.environ.get("SCENT_NOTE_PROMPTS")

    if ENV_NOTE_PROMPTS:
        NOTE_PROMPTS_RAW = ENV_NOTE_PROMPTS
    else:
        NOTE_PROMPTS_RAW = generate_visual_entities()
        os.environ["SCENT_NOTE_PROMPTS"] = NOTE_PROMPTS_RAW

    print(NOTE_PROMPTS_RAW)