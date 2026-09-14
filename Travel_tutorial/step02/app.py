import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(page_title="여행zip", page_icon="🏘️")

# 2. 사이드바 라디오 버튼 생성
menu = st.sidebar.radio("메뉴", ["한국", "미국", "중국", "일본"])

# 3. if / elif 조건문으로 메뉴별 화면 구성
if menu == "한국":
    st.header("🇰🇷 대한민국")
    st.write("사계절의 뚜렷한 아름다움과 전통, 현대 문화가 공존하는 여행지입니다.")
    st.image(
        "https://images.unsplash.com/photo-1546874177-9e664107314e?auto=format&fit=crop&w=800&h=450&q=80",
        caption="대한민국 서울 도심과 남산타워",
        use_container_width=True
    )
    st.link_button("대한민국 관광청 공식 사이트 방문", "https://korean.visitkorea.or.kr")

elif menu == "미국":
    st.header("🇺🇸 미국")
    st.write("광활한 대자연과 세계적인 대도시 문화를 동시에 만날 수 있는 여행지입니다.")
    st.image(
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=800&h=450&q=80",
        caption="미국 샌프란시스코",
        use_container_width=True
    )
    st.link_button("미국 관광청 공식 사이트 방문", "https://www.gousa.or.kr")

elif menu == "중국":
    st.header("🇨🇳 중국")
    st.write("장대한 자연경관과 유구한 역사 유적, 풍부한 미식을 즐길 수 있는 여행지입니다.")
    st.image(
        "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?auto=format&fit=crop&w=800&h=450&q=80",
        caption="중국 만리장성",
        use_container_width=True
    )
    # 기존 cnto.or.kr 대신 안정적인 공식 포털 링크로 변경
    st.link_button("중국 관광청 공식 사이트 방문", "https://korean.visitbeijing.com.cn")

elif menu == "일본":
    st.header("🇯🇵 일본")
    st.write("고즈넉한 온천과 정갈한 미식 문화, 다채로운 골목 풍경이 있는 여행지입니다.")
    st.image(
        "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&h=450&q=80",
        caption="일본 교토",
        use_container_width=True
    )
    st.link_button("일본 관광청 공식 사이트 방문", "https://www.japan.travel/ko/kr/")