import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent
PYTHON = sys.executable

def run(script):
    subprocess.run(
        [PYTHON, script],
        cwd=BASE_DIR,
        check=True
    )

print("▶ Generating note images...")
run("sd_generate.py")

print("▶ Stacking images...")
run("stack.py")

print("✅ SCENT STACK GENERATED")