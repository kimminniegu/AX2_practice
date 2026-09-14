import streamlit as st

st.set_page_config(page_title="여행zip", page_icon="🏘️")

korea_page = st.Page("view/korea.py", title="한국", icon="🇰🇷", default=True) # 기본값 지정
us_page = st.Page("view/us.py", title="미국", icon="🇺🇸")
china_page = st.Page("view/china.py", title="중국", icon="🇨🇳")
japan_page = st.Page("view/japan.py", title="일본", icon="🇯🇵")

# 네비게이션 메뉴 가동(사이드바 메뉴가 자동으로 생김)
pg = st.navigation([korea_page, us_page, china_page, japan_page])
pg.run()