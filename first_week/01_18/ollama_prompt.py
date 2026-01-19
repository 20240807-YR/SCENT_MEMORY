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

def generate_visual_prompt(note_type, note_text):
    prompt = f"""
You are a system that converts perfume notes into abstract visual prompts for Stable Diffusion.

Strict rules:
- Abstract only
- No literal objects
- No flowers, fruits, woods, or named materials
- Use texture, light, motion, density, color, atmosphere
- Describe visual sensation, not smell
- One paragraph only
- No titles, no explanations

Note type: {note_type}

Note description:
{note_text}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()

def generate_all_prompts():
    notes = load_perfume_notes()
    return {
        "top": generate_visual_prompt("top", notes["top"]),
        "middle": generate_visual_prompt("middle", notes["middle"]),
        "base": generate_visual_prompt("base", notes["base"]),
    }

if __name__ == "__main__":
    prompts = generate_all_prompts()
    for k, v in prompts.items():
        print(f"{k.upper()} PROMPT:\n{v}\n")