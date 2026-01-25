import streamlit as st
import time
import base64
from pathlib import Path
import streamlit.components.v1 as components
#from genai import generate_aura_narration

st.set_page_config(page_title="SCENT AURA", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_brand" not in st.session_state:
    st.session_state.selected_brand = None
if "show_motion" not in st.session_state:
    st.session_state.show_motion = False
if "narration_done" not in st.session_state:
    st.session_state.narration_done = False
if "narration_text" not in st.session_state:
    st.session_state.narration_text = ""

FRAGRANCES = {
    "lancome": {
        "name": "Lancôme – La Vie Est Belle",
        "keywords": ["radiant", "soft expansion", "warm sweetness"],
        "narration": (
            "Golden sweetness expands slowly, like light diffusing through silk. "
            "Warm air settles and lingers, leaving a soft trace of presence."
        )
    },
    "ysl": {
        "name": "YSL – Libre EDP",
        "keywords": ["vertical tension", "sharp floral", "bold energy"],
        "narration": (
            "A journey that begins with cool air and ends on warm skin. The opening bursts with light as mandarin and neroli cut through the space, while lavender brings a refined balance. As the scent unfolds, jasmine and orange blossom form the heart, revealing a floral warmth and quiet sensuality. In the final stage, white musk, tonka bean, and vanilla cling to the skin, leaving a soft yet deep trail. The fragrance ultimately becomes a memory of freedom and strength softened by warmth, where light and body heat coexist."
        )
    },
    "margiela": {
        "name": "Maison Margiela – Lazy Sunday Morning",
        "keywords": ["clean skin", "soft diffusion", "quiet intimacy"],
        "narration": (
            "Soft air settles on fabric and skin. "
            "The space becomes still, intimate, and almost transparent."
        )
    },
}


def image_to_base64(path: Path) -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"

def go_home():
    st.session_state.page = "home"
    st.session_state.selected_brand = None
    st.session_state.show_motion = False
    st.session_state.narration_done = False
    st.session_state.narration_text = ""
    st.rerun()

def go_result(key: str):
    st.session_state.page = "detail"
    st.session_state.selected_brand = key
    st.session_state.show_motion = False
    st.session_state.narration_done = False
    st.session_state.narration_text = ""
    st.rerun()

def toggle_motion():
    st.session_state.show_motion = not st.session_state.show_motion
    st.rerun()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Montserrat:wght@300;400&display=swap');
    html, body, .stApp {
        background-color: #0e0e0e;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
        overflow-x: hidden;
    }
    h1, h2, h3 {
        font-family: 'Cinzel', serif;
        letter-spacing: 0.15em;
    }
    #MainMenu, footer, header {
        visibility: hidden;
        height: 0;
    }
    .card {
        border: 1px solid rgba(255,255,255,0.18);
        padding: 20px;
        transition: 0.3s;
        text-align: center;
    }
    .card:hover {
        border-color: #d4af37;
        background: rgba(255,255,255,0.03);
    }
    .card img {
        width: 100%;
        height: 360px;
        object-fit: cover;
        margin-bottom: 20px;
    }
    .card-title {
        font-family: 'Cinzel', serif;
        font-size: 1.1rem;
        line-height: 1.4;
    }
    .gold-btn button {
        border: 1px solid #d4af37 !important;
        background: transparent !important;
        color: #ffffff !important;
        padding: 0.6em 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def render_home():
    st.markdown("<h1 style='text-align:center; margin-top:60px;'>SCENT AURA</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; opacity:0.6; margin-bottom:80px; font-size:1.1rem;'>Select a fragrance to reveal its digital aura</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    for col, key in zip(cols, FRAGRANCES.keys()):
        with col:
            brand_dir = Path(f"assets/brands/{key}")
            imgs = list(brand_dir.glob("*.png")) + list(brand_dir.glob("*.jpg"))
            if imgs:
                img_src = image_to_base64(imgs[0])
            else:
                img_src = "https://source.unsplash.com/600x800/?perfume"

            st.markdown(
                f"""
                <div class="card">
                    <img src="{img_src}">
                    <div class="card-title">{FRAGRANCES[key]['name']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Explore", key=f"btn_{key}", use_container_width=True):
                go_result(key)


def render_detail():
    brand = FRAGRANCES[st.session_state.selected_brand]

    if st.button("← BACK"):
        go_home()

    st.markdown(f"<h2 style='text-align:center; margin:30px 0;'>{brand['name']}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        brand_dir = Path(f"assets/brands/{st.session_state.selected_brand}")
        imgs = list(brand_dir.glob("*.png")) + list(brand_dir.glob("*.jpg"))
        if imgs:
            img_src = image_to_base64(imgs[0])
        else:
            img_src = "https://source.unsplash.com/800x1000/?perfume"

        st.markdown(
            f"""
            <div style="border:1px solid rgba(255,255,255,0.2);">
                <img src="{img_src}" style="width:100%; height:520px; object-fit:cover;">
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("### Description")
        st.markdown(
            "<p style='opacity:0.75; line-height:1.7;'>An interpretation of scent structure and emotional diffusion, rendered through generative analysis.</p>",
            unsafe_allow_html=True,
        )

        st.markdown("### SCENT AI Analysis")

        if not st.session_state.narration_done:
            #narration = generate_aura_narration(
            #    fragrance_name=brand["name"],
            #    keywords=brand["keywords"],
            #)
            narration = brand["narration"]

            placeholder = st.empty()
            with st.spinner("Gemini is analyzing the scent structure..."):
                time.sleep(1.2)

            rendered = ""
            for ch in narration:
                rendered += ch
                placeholder.markdown(
                    f"<div style='line-height:1.8; font-size:1.05rem;'>{rendered}▌</div>",
                    unsafe_allow_html=True,
                )
                time.sleep(0.02)

            placeholder.markdown(
                f"<div style='line-height:1.8; font-size:1.05rem;'>{rendered}</div>",
                unsafe_allow_html=True,
            )

            st.session_state.narration_text = rendered
            st.session_state.narration_done = True
        else:
            st.markdown(
                f"<div style='line-height:1.8; font-size:1.05rem;'>{st.session_state.narration_text}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin:60px 0;'></div>", unsafe_allow_html=True)

    st.markdown("<div class='gold-btn'>", unsafe_allow_html=True)
    if st.button("ENTER SCENT CANVAS", use_container_width=True):
        toggle_motion()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.show_motion:
        try:
            html_code = Path("index.html").read_text(encoding="utf-8")
            components.html(html_code, height=600, scrolling=False)
        except Exception:
            st.error("index.html 파일을 불러올 수 없습니다.")


if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "detail":
    render_detail()