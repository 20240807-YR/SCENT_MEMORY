# genai.py
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are a curator narrating a fragrance as an abstract installation.
Never recommend or persuade.
Never address the viewer directly.
Never mention AI, models, or technology.
Describe the scent as light, texture, space, and atmosphere.
Tone must be restrained, poetic, and gallery-like.
Limit the response to 2–3 sentences.
"""

def generate_aura_narration(fragrance_name: str, keywords: list[str]) -> str:
    # Defensive handling
    if not keywords:
        keywords = ["light", "air", "memory"]

    user_prompt = f"""
Fragrance name: {fragrance_name}
Aura keywords: {", ".join(keywords)}

Interpret this fragrance as a visual and spatial aura,
as if describing an installation in a luxury exhibition space.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
            temperature=0.65,
        )

        text = response.choices[0].message.content.strip()

        # Hard trim in case the model ignores instructions
        sentences = text.split(".")
        trimmed = ".".join(sentences[:3]).strip()
        if not trimmed.endswith("."):
            trimmed += "."

        return trimmed

    except Exception:
        # Fallback text to keep demo stable
        return (
            "A quiet composition of light and air unfolds in the space. "
            "Soft textures linger like memory on skin, suspended between presence and absence."
        )