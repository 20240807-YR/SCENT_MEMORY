# app.py

import os
import streamlit as st
from PIL import Image
import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent
IMAGE_OUT = BASE_DIR / "image" / "main" / "scent_stack.png"
PYTHON = sys.executable

st.set_page_config(layout="wide")
st.title("SCENT × CONTEXT DEMO")

temp = st.number_input("Temperature (°C)", value=22)
humidity = st.number_input("Humidity (%)", value=55)
sky = st.selectbox("Sky", ["Clear", "Cloudy", "Rainy"])

image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if image_file is not None:
    input_image = Image.open(image_file)
    st.subheader("Input Photo")
    st.image(input_image, width=400)

run = st.button("Run Demo")

if run:
    with st.spinner("Generating scent visualization..."):
        try:
            subprocess.run(
                [PYTHON, "run_demo.py"],
                cwd=BASE_DIR,
                check=True,
                env=os.environ.copy()
            )
        except subprocess.CalledProcessError:
            st.error("Pipeline failed. Check terminal output.")
            st.stop()

    if IMAGE_OUT.exists():
        st.subheader("Scent Visualization (Top / Middle / Base)")
        result_image = Image.open(IMAGE_OUT)
        st.image(result_image, use_column_width=True)
    else:
        st.error("Scent image not generated.")