import os
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# 1. .env 기본값 로드 및 세션 상태 초기화 (날씨, 환율 2가지만 관리)
load_dotenv()

if "weather_key" not in st.session_state:
    st.session_state.weather_key = os.getenv("OPENWEATHER_API_KEY", "")
if "exchange_key" not in st.session_state:
    st.session_state.exchange_key = os.getenv("EXCHANGERATE_API_KEY", "")

# 페이지 기본 설정
st.set_page_config(page_title="TripPulse - 글로벌 여행자 비서", page_icon="✈️", layout="wide")

# 2. 사이드바: API 상태 대시보드 (지도 키 불필요 안내 포함)
st.sidebar.title("🔐 API 연동 현황")

def render_status(label, key_val):
    if key_val and len(key_val.strip()) > 0:
        st.sidebar.markdown(f"- **{label}**: 🟢 `연동 완료`")
        return True
    else:
        st.sidebar.markdown(f"- **{label}**: 🔴 `키 필요`")
        return False

# 지도/장소는 키 없이 무료 제공됨을 표시
st.sidebar.markdown("- **글로벌 지도/검색 (Folium & OSM)**: 🟢 `API 키 불필요 (무료)`")
weather_ok = render_status("실시간 날씨 (OpenWeather)", st.session_state.weather_key)
exchange_ok = render_status("실시간 환율 (ExchangeRate)", st.session_state.exchange_key)

st.sidebar.divider()

all_ready = weather_ok and exchange_ok
expander_title = "⚙️ API 키 관리 / 변경" if all_ready else "⚠️ API 키 등록 / 수정 필요"

with st.sidebar.expander(expander_title, expanded=not all_ready):
    st.caption("날씨 및 환율 API 키를 확인/수정하세요.")
    
    new_weather = st.text_input(
        "OpenWeatherMap API Key",
        value=st.session_state.weather_key,
        type="password",
        placeholder="OpenWeather 키 입력"
    )
    new_exchange = st.text_input(
        "ExchangeRate-API Key",
        value=st.session_state.exchange_key,
        type="password",
        placeholder="ExchangeRate 키 입력"
    )
    
    if st.button("설정 저장", use_container_width=True):
        st.session_state.weather_key = new_weather
        st.session_state.exchange_key = new_exchange
        st.success("API 키 설정이 업데이트되었습니다!")
        st.rerun()

# 3. 장소 검색 함수 (OpenStreetMap Nominatim - API 키 불필요)
@st.cache_data(ttl=600)
def search_places_free(query):
    """전 세계 무료 장소 검색 (OpenStreetMap 기반)"""
    if not query:
        return []
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "TripPulse_Streamlit_App/1.0"}
    params = {
        "q": query,
        "format": "json",
        "limit": 5,
        "addressdetails": 1
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            results = []
            for item in response.json():
                results.append({
                    "name": item.get("display_name", "").split(",")[0],
                    "address": item.get("display_name", ""),
                    "lat": float(item["lat"]),
                    "lon": float(item["lon"])
                })
            return results
    except Exception:
        return []
    return []

# 4. 날씨 & 환율 API 호출 함수
@st.cache_data(ttl=600)
def get_weather(lat, lon, api_key):
    """OpenWeatherMap API: 전 세계 실시간 날씨"""
    if not api_key:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key.strip(),
        "units": "metric",
        "lang": "kr"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

@st.cache_data(ttl=3600)
def get_exchange_rates(api_key, base_currency="USD"):
    """ExchangeRate-API: 전 세계 실시간 환율"""
    if not api_key:
        return None
    url = f"https://v6.exchangerate-api.com/v6/{api_key.strip()}/latest/{base_currency}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("conversion_rates", {})
    except Exception:
        return None
    return None

# 5. 메인 화면 및 검색
st.title("🌍 TripPulse 글로벌 여행자 대시보드")
st.caption("Folium 오픈 지도를 기반으로 국내/해외 여행지의 날씨와 환율을 확인하세요.")

search_query = st.text_input("🔍 방문할 목적지 또는 도시를 검색하세요 (예: 제주공항, 에펠탑, 도쿄타워, 런던아이)", value="에펠탑")

# 기본 위치값 (검색 전 fallback)
selected_lat = 48.8584
selected_lon = 2.2945
place_name = "Eiffel Tower"
place_address = "Champ de Mars, 5 Av. Anatole France, 75007 Paris, France"

if search_query:
    places = search_places_free(search_query)
    if places:
        place_options = {f"{p['name']} ({p['address'][:50]}...)": p for p in places}
        selected_key = st.selectbox("검색 결과 선택", list(place_options.keys()))
        target = place_options[selected_key]
        selected_lat = target["lat"]
        selected_lon = target["lon"]
        place_name = target["name"]
        place_address = target["address"]
    else:
        st.info("검색 결과가 없습니다. 다른 검색어나 영문 명칭으로 검색해 보세요.")

st.divider()

# 6. 탭 구성 (기본: 지도)
tab_map, tab_weather, tab_exchange = st.tabs(["📍 지도 & 장소 탐색 (Folium)", "⛅ 현지 실시간 날씨", "💱 실시간 환율 계산기"])

# --- TAB 1: Folium 오픈 지도 ---
with tab_map:
    st.subheader(f"📍 {place_name}")
    st.caption(f"**전체 주소:** {place_address}")
    
    # Folium 지도 생성 (API 키 없이 무료 렌더링)
    m = folium.Map(location=[selected_lat, selected_lon], zoom_start=15)
    folium.Marker(
        [selected_lat, selected_lon],
        popup=f"<b>{place_name}</b><br>{place_address}",
        tooltip=place_name,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    st_folium(m, width=None, height=480)

# --- TAB 2: 날씨 ---
with tab_weather:
    st.subheader(f"⛅ {place_name} 주변 실시간 날씨")
    
    if not st.session_state.weather_key:
        st.warning("⚠️ 사이드바에서 **OpenWeatherMap API Key**를 등록해야 날씨 정보를 확인할 수 있습니다.")
    else:
        weather_data = get_weather(selected_lat, selected_lon, st.session_state.weather_key)
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
            st.error("날씨 데이터를 가져오지 못했습니다. API 키가 유효한지 확인해주세요.")

# --- TAB 3: 환율 계산기 ---
with tab_exchange:
    st.subheader("💱 실시간 환율 계산기")
    
    if not st.session_state.exchange_key:
        st.warning("⚠️ 사이드바에서 **ExchangeRate-API Key**를 등록해야 실시간 환율을 조회할 수 있습니다.")
    else:
        rates = get_exchange_rates(st.session_state.exchange_key, "USD")
        if rates:
            supported_currencies = [
                "KRW", "USD", "JPY", "EUR", "GBP", "CNY", 
                "THB", "VND", "TWD", "SGD", "PHP", "AUD", "CAD", "CHF"
            ]
            
            col_cur1, col_cur2 = st.columns(2)
            with col_cur1:
                from_cur = st.selectbox("보유/현지 통화 (From)", supported_currencies, index=supported_currencies.index("EUR"))
            with col_cur2:
                to_cur = st.selectbox("환산 통화 (To)", supported_currencies, index=supported_currencies.index("KRW"))
            
            amount = st.number_input(f"환산할 금액 ({from_cur})", min_value=0.0, value=100.0, step=10.0)
            
            from_rate = rates.get(from_cur, 1.0)
            to_rate = rates.get(to_cur, 1.0)
            converted_amount = (amount / from_rate) * to_rate
            unit_rate = to_rate / from_rate
            
            st.success(f"### 계산 결과: **{converted_amount:,.2f} {to_cur}**")
            st.caption(f"적용 기준 환율: 1 {from_cur} = {unit_rate:,.4f} {to_cur}")
        else:
            st.error("환율 데이터를 가져오지 못했습니다. API 키가 유효한지 확인해주세요.")