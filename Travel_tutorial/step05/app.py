import streamlit as st
from src.data.countries import COUNTRIES_DATA
from src.components.card import render_country_card

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="글로벌 여행 안내 가이드",
    page_icon="✈️",
    layout="wide"
)

# 2. 헤더 영역
st.title("✈️ 글로벌 여행 안내 센터")
st.caption("한국, 미국, 일본, 중국의 주요 여행 정보와 공식 관광청 웹사이트 링크를 제공합니다.")

st.divider()

# 3. 탭 구성 및 각 국가별 카드 렌더링
tabs = st.tabs([f"{data['flag']} {name}" for name, data in COUNTRIES_DATA.items()])

for tab, (country_name, country_data) in zip(tabs, COUNTRIES_DATA.items()):
    with tab:
        render_country_card(country_name, country_data)