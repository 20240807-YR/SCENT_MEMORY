# llm_explain.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_explanation(weather, perfume, is_match: bool) -> str:
    if not is_match:
        return "This fragrance may feel less balanced under today's weather conditions."

    prompt = f"""
You are a fragrance explanation module.

Weather:
- Temperature: {weather["temp"]}°C
- Humidity: {weather["humidity"]}%
- Sky: {weather["sky"]}

Perfume:
Name: {perfume["name"]}
Description:
{perfume["description"]}

Task:
Explain in 2–3 calm, sensory sentences why this fragrance suits today's weather.
No marketing tone.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
    )

    return response.choices[0].message.content.strip()