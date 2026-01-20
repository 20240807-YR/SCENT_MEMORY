# app.py

import os
import streamlit as st
from PIL import Image
import subprocess
from pathlib import Path
import sys
import json
import streamlit.components.v1 as components
from demo_weather import get_weather

BASE_DIR = Path(__file__).parent
IMAGE_OUT = BASE_DIR / "image" / "main" / "scent_stack.png"
PYTHON = sys.executable


# Helper to ensure flower images exist in assets directory
def ensure_flower_images():
    assets_dir = BASE_DIR / "assets"
    assets_dir.mkdir(exist_ok=True)

    color_map = {
        "top.png": (255, 217, 102),     # citrus
        "middle.png": (201, 182, 228),  # lavender
        "base.png": (142, 127, 109),    # woody
    }

    for name, rgb in color_map.items():
        path = assets_dir / name
        if not path.exists():
            result = subprocess.run(
                [
                    PYTHON,
                    "-m",
                    "sd_generate",
                    "--note",
                    name.replace(".png", ""),
                    "--out",
                    str(path)
                ],
                cwd=BASE_DIR,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"sd_generate failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
                )

st.set_page_config(layout="wide")
st.title("SCENT × CONTEXT DEMO")

date = st.date_input("Date")
location = st.selectbox(
    "Location",
    ["서울", "부산", "광주", "창원"]
)

LOCATION_GRID = {
    "서울": (60, 127),
    "부산": (98, 76),
    "광주": (58, 74),
    "창원": (90, 77),
}

nx, ny = LOCATION_GRID[location]
weather = get_weather(date, nx, ny)

temperature = weather.get("T1H", 8)
humidity = weather.get("REH", 55)
sky = weather.get("SKY", "1")

st.text_input("Temperature (°C)", value=str(temperature), disabled=True)
st.text_input("Humidity (%)", value=str(humidity), disabled=True)
st.text_input("Sky", value=str(sky), disabled=True)

image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if image_file is not None:
    input_image = Image.open(image_file)
    st.subheader("Input Photo")
    st.image(input_image, width=400)

run = st.button("Run Demo")

if run:
    ensure_flower_images()
    with st.spinner("Generating scent visualization..."):
        try:
            json_path = BASE_DIR / "lazy_sunday_morning.json"
            with open(json_path, "r") as f:
                prompt_json = json.load(f)

            _ = subprocess.run(
                [PYTHON, "-m", "ollama_prompt", "generate_visual_entities"],
                input=json.dumps(prompt_json),
                capture_output=True,
                text=True,
                check=False,
                cwd=BASE_DIR,
                env=os.environ.copy()
            )
            visual_entities = prompt_json["notes"]
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
            st.stop()

    st.markdown("---")
    st.subheader("SCENT CANVAS")

    HTML_FILE = BASE_DIR / "index.html"

    if not HTML_FILE.exists():
        st.error("index.html 파일을 찾을 수 없습니다.")
    else:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            index_html = f.read()
        # 클릭 가능한 카드 UI
        card_html = f"""
        <style>
          .scent-preview {{
            width: 100%;
            max-width: 720px;
            margin: 0 auto;
            padding: 24px;
            border-radius: 6px;
            background: linear-gradient(135deg, #141418, #0d0d10);
            box-shadow: 0 12px 40px rgba(0,0,0,0.4);
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
          }}

          .scent-preview:hover {{
            transform: translateY(-2px);
            box-shadow: 0 18px 60px rgba(0,0,0,0.6);
          }}

          .scent-preview h3 {{
            margin: 0 0 8px 0;
            color: #ffffff;
            font-family: "Times New Roman", serif;
            letter-spacing: 0.2em;
            font-size: 14px;
          }}

          .scent-preview p {{
            margin: 0;
            color: #bbbbbb;
            font-size: 12px;
            font-family: sans-serif;
          }}
        </style>

        <div class="scent-preview"
             onclick="window.open(window.location.origin + '/_stcore/streamlit_static/index.html', '_blank')">
          <h3>SCENT CANVAS</h3>
          <p>Click to open interactive scent visualization</p>
        </div>
        """

        components.html(card_html, height=140)
        components.html(index_html, height=900, scrolling=False)