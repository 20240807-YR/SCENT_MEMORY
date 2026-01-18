# prompt_builder.py
import json

def build_prompt(note_name, note_data, weather_context=None):
    base_prompt = f"""
Abstract visual interpretation of a fragrance {note_name} note.
{note_data["visual_translation"]}
Sensory keywords: {", ".join(note_data["sensory_keywords"])}.
No objects. No text. No people.
Pure abstract diffusion.
"""

    if weather_context:
        base_prompt += f"\nEnvironmental context: {weather_context}."

    return base_prompt.strip()


def load_perfume_json(path="lazy_sunday_morning.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    data = load_perfume_json()

    for note in ["top", "middle", "base"]:
        prompt = build_prompt(
            note_name=note,
            note_data=data["notes"][note],
            weather_context="soft morning air, low contrast light"
        )
        print(f"\n[{note.upper()} PROMPT]\n")
        print(prompt)