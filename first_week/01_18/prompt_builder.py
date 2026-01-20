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


def build_note_prompts(perfume: dict, weather: dict):
    weather_context = ""

    if weather:
        temp = weather.get("T1H", "")
        reh = weather.get("REH", "")
        sky = weather.get("SKY", "")
        weather_context = f"temperature {temp}, humidity {reh}, sky {sky}"

    return {
        "top": build_prompt(
            "top",
            perfume["notes"]["top"],
            weather_context
        ),
        "middle": build_prompt(
            "middle",
            perfume["notes"]["middle"],
            weather_context
        ),
        "base": build_prompt(
            "base",
            perfume["notes"]["base"],
            weather_context
        ),
    }


if __name__ == "__main__":
    data = load_perfume_json()
    prompts = build_note_prompts(
        data,
        {"T1H": 22, "REH": 55, "SKY": "1"}
    )

    for k, v in prompts.items():
        print(f"\n[{k.upper()}]\n{v}")