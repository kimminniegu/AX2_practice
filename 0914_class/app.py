import os
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# .env 로드
load_dotenv()
KAKAO_REST_KEY = os.getenv("KAKAO_REST_API_KEY")

st.set_page_config(page_title="REST API 키워드/주소 검색 지도", layout="wide")
st.title("📍 카카오 REST API + 일반 지도 연동")

if not KAKAO_REST_KEY:
    st.error(".env 파일에 KAKAO_REST_API_KEY를 설정해주세요!")
    st.stop()

# 카카오 로컬 REST API: 키워드 검색 함수
def search_places(query):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_KEY}"}
    params = {"query": query, "size": 15}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("documents", [])
    return []

# 검색창 UI
query = st.text_input("검색할 장소나 주소를 입력하세요 (예: 강남역 맛집, 서울시청)", value="판교역")

if query:
    results = search_places(query)
    
    if results:
        col1, col2 = st.columns([1, 2])
        
        # 첫 번째 검색 결과를 지도 중심 좌표로 설정
        center_lat = float(results[0]["y"])
        center_lng = float(results[0]["x"])
        
        # Folium 지도 객체 생성 (OpenStreetMap 기반 일반 지도)
        m = folium.Map(location=[center_lat, center_lng], zoom_start=14)
        
        # 검색된 모든 결과에 마커 추가
        for place in results:
            p_lat = float(place["y"])
            p_lng = float(place["x"])
            p_name = place["place_name"]
            p_addr = place.get("road_address_name") or place.get("address_name")
            p_url = place.get("place_url", "")
            
            popup_html = f"""
            <div style="font-family: sans-serif; width: 180px;">
                <b>{p_name}</b><br>
                <span style="font-size:12px; color:gray;">{p_addr}</span><br>
                <a href="{p_url}" target="_blank" style="font-size:12px; color:blue;">카카오맵 상세 보기</a>
            </div>
            """
            
            folium.Marker(
                location=[p_lat, p_lng],
                tooltip=p_name,
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)
        
        # 좌측: 검색 목록 표시
        with col1:
            st.subheader(f"검색 결과 ({len(results)}건)")
            for i, place in enumerate(results):
                st.write(f"**{i+1}. {place['place_name']}**")
                st.caption(place.get("road_address_name") or place.get("address_name"))
                st.divider()
                
        # 우측: 지도 표시
        with col2:
            st.subheader("지도")
            st_folium(m, width=700, height=500)
            
    else:
        st.warning("검색 결과가 없습니다.")