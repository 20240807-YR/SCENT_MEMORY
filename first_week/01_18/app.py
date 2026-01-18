import os
import streamlit as st
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

st.set_page_config(layout="wide")
st.title("SCENT × CONTEXT DEMO")

temp = st.number_input("Temperature (°C)", value=22)
humidity = st.number_input("Humidity (%)", value=55)
sky = st.selectbox("Sky", ["Clear", "Cloudy", "Rainy"])

image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if "run" not in st.session_state:
    st.session_state.run = False

if st.button("Run Demo", key="run_demo"):
    st.session_state.run = True

if st.session_state.run and image_file:
    image = Image.open(image_file)

    prompt = f"""
You are a fragrance expert.

Weather:
- Temperature: {temp}°C
- Humidity: {humidity}%
- Sky: {sky}

Tasks:
1. Recommend ONE perfume
2. Explain why this weather suits it
3. Describe the emotion it evokes
4. Explain why the uploaded image matches the scent

Use calm, sensory language.
No marketing tone.
3 short paragraphs.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # ← 안정 + 멀티모달
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_file.getvalue(),
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    st.subheader("Recommended Fragrance")
    st.markdown(response.choices[0].message.content)

    st.subheader("Visual Context")
    st.image(image, use_column_width=True)