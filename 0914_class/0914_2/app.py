import os
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

# 페이지 기본 설정
st.set_page_config(page_title="TripPulse - 여행자 올인원 비서", page_icon="✈️", layout="wide")

# 2. API 호출 함수 (캐싱 적용)
@st.cache_data(ttl=600)
def search_kakao_places(query):
    """카카오 로컬 API: 장소 키워드 검색"""
    if not KAKAO_REST_API_KEY:
        return []
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"query": query, "size": 5}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("documents", [])
    return []

@st.cache_data(ttl=600)
def get_weather(lat, lon):
    """OpenWeatherMap API: 실시간 날씨"""
    if not OPENWEATHER_API_KEY:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

@st.cache_data(ttl=3600)
def get_exchange_rates(base_currency="USD"):
    """ExchangeRate-API: 실시간 환율 정보"""
    if not EXCHANGERATE_API_KEY:
        return None
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("conversion_rates", {})
    return None

# 3. 메인 헤더 및 목적지 검색 영역
st.title("🌍 TripPulse 여행자 대시보드")
st.caption("선택한 목적지를 기준으로 지도, 날씨, 환율 정보를 탭별로 확인하세요.")

search_query = st.text_input("🔍 방문할 목적지 또는 장소를 검색하세요", value="제주공항")

selected_lat = 33.5066
selected_lon = 126.4932
place_name = "제주국제공항"
place_address = "제주특별자치도 제주시 공항로 2"

if search_query:
    places = search_kakao_places(search_query)
    if places:
        place_options = {f"{p['place_name']} ({p.get('address_name', '')})": p for p in places}
        selected_key = st.selectbox("검색 결과 선택", list(place_options.keys()))
        target = place_options[selected_key]
        selected_lat = float(target["y"])
        selected_lon = float(target["x"])
        place_name = target["place_name"]
        place_address = target.get("address_name", "")
    else:
        st.info("검색 결과가 없거나 KAKAO_REST_API_KEY 설정이 필요합니다. (기본 위치로 표시)")

st.divider()

# 4. 탭 구성 (기본 탭: 지도)
tab_map, tab_weather, tab_exchange = st.tabs(["📍 지도 & 장소 탐색", "⛅ 실시간 날씨", "💱 환율 계산기"])

# --- TAB 1: 지도 & 장소 탐색 (기본 활성화) ---
with tab_map:
    st.subheader(f"📍 {place_name}")
    st.write(f"**상세 주소:** {place_address}")
    
    m = folium.Map(location=[selected_lat, selected_lon], zoom_start=15)
    folium.Marker(
        [selected_lat, selected_lon],
        popup=f"<b>{place_name}</b><br>{place_address}",
        tooltip=place_name,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    st_folium(m, width=None, height=480)

# --- TAB 2: 실시간 날씨 ---
with tab_weather:
    st.subheader(f"⛅ {place_name} 주변 실시간 날씨")
    weather_data = get_weather(selected_lat, selected_lon)
    
    if weather_data:
        main = weather_data.get("main", {})
        weather_desc = weather_data.get("weather", [{}])[0].get("description", "")
        temp = main.get("temp", 0.0)
        feels_like = main.get("feels_like", 0.0)
        humidity = main.get("humidity", 0)
        wind_speed = weather_data.get("wind", {}).get("speed", 0.0)
        icon_code = weather_data.get("weather", [{}])[0].get("icon", "01d")
        
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            st.image(f"http://openweathermap.org/img/wn/{icon_code}@2x.png", width=90)
            st.metric(label="현재 기온", value=f"{temp:.1f} °C", delta=f"체감 {feels_like:.1f} °C")
        with col_w2:
            st.metric(label="날씨 상태", value=weather_desc.capitalize())
            st.metric(label="습도", value=f"{humidity} %")
        with col_w3:
            st.metric(label="최고 / 최저", value=f"{main.get('temp_max', 0.0):.1f}°C / {main.get('temp_min', 0.0):.1f}°C")
            st.metric(label="풍속", value=f"{wind_speed} m/s")
    else:
        st.warning("날씨 정보를 불러올 수 없습니다. OPENWEATHER_API_KEY를 확인하세요.")

# --- TAB 3: 환율 계산기 ---
with tab_exchange:
    st.subheader("💱 실시간 환율 계산기")
    rates = get_exchange_rates("USD")
    
    if rates:
        supported_currencies = ["KRW", "USD", "JPY", "EUR", "CNY", "GBP", "VND", "THB", "TWD", "AUD"]
        
        col_cur1, col_cur2 = st.columns(2)
        with col_cur1:
            from_cur = st.selectbox("보유 통화 (From)", supported_currencies, index=supported_currencies.index("USD"))
        with col_cur2:
            to_cur = st.selectbox("환산할 통화 (To)", supported_currencies, index=supported_currencies.index("KRW"))
        
        amount = st.number_input(f"환산할 금액 ({from_cur})", min_value=0.0, value=100.0, step=10.0)
        
        # USD 기준 환율 변환 계산
        from_rate = rates.get(from_cur, 1.0)
        to_rate = rates.get(to_cur, 1.0)
        converted_amount = (amount / from_rate) * to_rate
        unit_rate = to_rate / from_rate
        
        st.success(f"### 계산 결과: **{converted_amount:,.2f} {to_cur}**")
        st.caption(f"적용 기준 환율: 1 {from_cur} = {unit_rate:,.4f} {to_cur}")
    else:
        st.warning("환율 정보를 불러올 수 없습니다. EXCHANGERATE_API_KEY를 확인하세요.")