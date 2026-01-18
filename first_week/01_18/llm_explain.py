import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_explanation(weather, perfume, is_match: bool) -> str:
    if not is_match:
        return "This fragrance may feel less balanced under today's weather conditions."

    prompt = f"""
You are a fragrance recommendation assistant.

Weather:
- Temperature: {weather['temp']}°C
- Humidity: {weather['humidity']}%
- Sky: {weather['sky']}

Perfume:
Name: {perfume['name']}
Description:
{perfume['description']}

Explain in 2–3 sentences why this fragrance suits today's weather.
Use calm, sensory language.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
    )

    return response.choices[0].message.content.strip()