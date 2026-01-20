# run_demo.py

import sys
import subprocess
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
PYTHON = sys.executable


def run(script_name, env=None):
    subprocess.run(
        [PYTHON, str(BASE_DIR / script_name)],
        cwd=BASE_DIR,
        env=env,
        check=True
    )


from demo_weather import get_weather
from prompt_builder import build_note_prompts

print("▶ Loading weather...")
weather = get_weather()

print("▶ Loading perfume data...")
with open(BASE_DIR / "lazy_sunday_morning.json", "r", encoding="utf-8") as f:
    perfume = json.load(f)

print("▶ Building note prompts...")
note_prompts = build_note_prompts(
    perfume=perfume,
    weather=weather
)

print("▶ Generating note images...")
env = os.environ.copy()
env["SCENT_NOTE_PROMPTS"] = json.dumps(note_prompts, ensure_ascii=False)

run("sd_generate.py", env=env)

print("▶ Stacking images...")
run("stack.py")

print("✅ SCENT STACK GENERATED")