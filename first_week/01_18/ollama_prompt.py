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
You are a system that designs visual entities for an interactive, animated visualization.

STRICT RULES:
- Output JSON only
- No markdown
- No explanation text
- No trailing comments
- No natural language outside JSON
- This JSON will be consumed directly by code

Each entity represents a perfume ingredient as an abstract moving visual object.

Allowed values:
shape: small_circle | grain | soft_wave | particle | fog | line
motion: fast_float | slow_drift | heavy_float | pulse | jitter
color: HEX string

Output format (MUST MATCH EXACTLY):

{{
  "top": [],
  "middle": [],
  "base": []
}}

Perfume notes:
{json.dumps(notes, ensure_ascii=False, indent=2)}
{weather_block}
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

    json.loads(output)

    return output


if __name__ == "__main__":
    print(generate_visual_entities())