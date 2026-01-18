# ollama_prompt.py
import subprocess

def generate_visual_prompts(notes_text):
    prompt = f"""
You are a system that converts perfume structure into abstract visual prompts.

Rules:
- No literal objects
- No flowers, fruits, wood depiction
- Abstract, texture, motion, color only

Perfume structure:
{notes_text}

Return format:
Top:
Middle:
Base:
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout


if __name__ == "__main__":
    notes = """
Top: citrus, aldehydes
Middle: floral
Base: woody, amber
"""
    prompts = generate_visual_prompts(notes)
    print(prompts)
