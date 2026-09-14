import streamlit as st
import os

def render_country_card(country_name: str, data: dict):
    st.subheader(f"{data['flag']} {country_name}")
    
    # 2단 레이아웃 (왼쪽: 이미지 / 오른쪽: 세부 정보)
    col1, col2 = st.columns([1.2, 1.8], gap="medium")
    
    with col1:
        if os.path.exists(data["image_file"]):
            st.image(data["image_file"], use_container_width=True)
        else:
            st.warning(f"이미지를 찾을 수 없습니다: {data['image_file']}")
            
    with col2:
        st.markdown(f"**🏛️ 수도:** {data['capital']}")
        st.markdown(f"**💰 통화:** {data['currency']}")
        st.markdown(f"**🗣️ 언어:** {data['language']}")
        st.write(data["description"])
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.link_button(
            label=f"🔗 {country_name} 공식 관광청 사이트 바로가기",
            url=data["official_site"],
            use_container_width=True
        )