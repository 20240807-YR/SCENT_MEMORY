import streamlit as st
st.write("앱 시작됨")

import streamlit as st
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("national_symbols.csv")

st.set_page_config(
    page_title="국가 상징 키오스크",
    layout="centered"
)

st.title("국가 상징 키오스크")
st.subheader("나라를 선택하면 국화와 국목을 보여줍니다")

# 나라 선택
country = st.selectbox(
    "나라를 선택하세요",
    df["country"].unique()
)

# 선택한 나라 데이터
row = df[df["country"] == country].iloc[0]

st.markdown("---")

# 결과 표시
col1, col2 = st.columns(2)

with col1:
    st.markdown("국화")
    st.markdown(f"{row['flower']}")

with col2:
    st.markdown("국목")
    st.markdown(f"{row['tree']}")

st.markdown("---")
st.caption("향수 데이터셋 · 국가 상징 기반")

