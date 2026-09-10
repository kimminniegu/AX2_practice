import base64
import os
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

# -------------------------------------------------------------
# 0. .env 환경변수 로드
# -------------------------------------------------------------
load_dotenv()
ENV_EXCHANGERATE_KEY = os.getenv("EXCHANGERATE_API_KEY", "")
ENV_OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# -------------------------------------------------------------
# 1. 페이지 설정 및 커스텀 폰트/스타일(CSS)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Global Currency & Weather Hub",
    page_icon="🧭",
    layout="wide"
)

# 로컬 폰트 파일을 Base64로 인코딩하여 CSS @font-face에 적용하는 함수
def get_font_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

font_file_name = "에이투지체-4Regular.otf"
font_base64 = get_font_base64(font_file_name)

if font_base64:
    font_css = f"""
    <style>
        @font-face {{
            font-family: 'AtoZ';
            src: url(data:font/opentype;charset=utf-8;base64,{font_base64}) format('opentype');
            font-weight: normal;
            font-style: normal;
        }}
        
        /* 1. 일반 텍스트 요소에만 커스텀 폰트 적용 */
        html, body, [class*="css"], div, p, h1, h2, h3, h4, h5, h6, input, button, select, label {{
            font-family: 'AtoZ', sans-serif !important;
        }}

        /* 2. Streamlit 기본 아이콘 폰트 보호 (텍스트 깨짐 현상 방지) */
        span:not([data-testid="stIconMaterial"]):not([class*="material-icons"]) {{
            font-family: 'AtoZ', sans-serif !important;
        }}
        [data-testid="stIconMaterial"], .material-symbols-rounded, .material-symbols-outlined, [class*="material-icons"] {{
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        }}

        .metric-card {{
            background: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 10px;
            padding: 14px;
            text-align: center;
        }}
        .weather-sidebar-card {{
            background: rgba(128, 128, 128, 0.08);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }}
    </style>
    """
    st.markdown(font_css, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .metric-card {
            background: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 10px;
            padding: 14px;
            text-align: center;
        }
        .weather-sidebar-card {
            background: rgba(128, 128, 128, 0.08);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. 통화 및 도시 매핑
# -------------------------------------------------------------
CURRENCY_CITY_MAP = {
    "KRW": {"name": "대한민국 원", "country": "한국", "city": "Seoul", "flag": "🇰🇷", "symbol": "₩"},
    "USD": {"name": "미국 달러", "country": "미국", "city": "New York", "flag": "🇺🇸", "symbol": "$"},
    "JPY": {"name": "일본 엔", "country": "일본", "city": "Tokyo", "flag": "🇯🇵", "symbol": "¥"},
    "EUR": {"name": "유럽연합 유로", "country": "유럽", "city": "Paris", "flag": "🇪🇺", "symbol": "€"},
    "CNY": {"name": "중국 위안", "country": "중국", "city": "Beijing", "flag": "🇨🇳", "symbol": "¥"},
}

WEATHER_DESC_KOR = {
    "온흐림": "흐림 (구름 많음)",
    "튼구름": "구름 조금",
    "조각구름": "구름 많음",
    "약간의 구름이 낀 하늘": "구름 조금",
    "실 비": "약한 비",
    "가벼운 비": "약한 비",
    "가벼운 눈": "약한 눈",
    "박무": "옅은 안개",
    "연무": "안개",
    "맑음": "맑음",
}

# -------------------------------------------------------------
# 3. API 데이터 조회 함수
# -------------------------------------------------------------
@st.cache_data(ttl=1800)
def get_exchange_rates(base_currency="USD", api_key=""):
    """환율 데이터 수집"""
    if api_key:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    else:
        url = f"https://open.er-api.com/v6/latest/{base_currency}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get("result") == "success" or "rates" in data:
            return data.get("conversion_rates") or data.get("rates")
    except Exception as e:
        st.error(f"환율 정보를 가져오는 중 오류 발생: {e}")
    return None

@st.cache_data(ttl=1800)
def get_weather_info(city_name, api_key):
    """도시별 실시간 날씨 수집 및 한국어 보정"""
    if not api_key:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "kr"
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code == 200:
            data = res.json()
            raw_desc = data["weather"][0]["description"]
            data["weather"][0]["description"] = WEATHER_DESC_KOR.get(raw_desc, raw_desc)
            return data
    except Exception:
        pass
    return None

# -------------------------------------------------------------
# 4. 사이드바 - [미니 날씨 카드] & [서비스 상태]
# -------------------------------------------------------------
with st.sidebar:
    st.header("🌤️ 현지 날씨 브리핑")
    
    if not ENV_OPENWEATHER_KEY:
        st.caption("⚠️ .env에 날씨 API 키가 설정되지 않았습니다.")
    else:
        selected_city_curr = st.selectbox(
            "도시 선택",
            options=list(CURRENCY_CITY_MAP.keys()),
            index=0,
            format_func=lambda x: f"{CURRENCY_CITY_MAP[x]['flag']} {CURRENCY_CITY_MAP[x]['city']} ({CURRENCY_CITY_MAP[x]['country']})"
        )
        
        city_info = CURRENCY_CITY_MAP[selected_city_curr]
        w_data = get_weather_info(city_info["city"], ENV_OPENWEATHER_KEY)
        
        if w_data:
            temp = w_data["main"]["temp"]
            feels_like = w_data["main"]["feels_like"]
            humidity = w_data["main"]["humidity"]
            wind_speed = w_data.get("wind", {}).get("speed", 0)
            desc = w_data["weather"][0]["description"]
            icon = w_data["weather"][0]["icon"]
            
            st.markdown(f"""
            <div class="weather-sidebar-card">
                <img src="https://openweathermap.org/img/wn/{icon}@2x.png" width="60" style="margin-bottom:-10px;">
                <h3 style="margin:0; font-size: 22px;">{temp:.1f}°C</h3>
                <p style="margin:0; font-size: 13px; color: #888;">{desc}</p>
                <hr style="margin:8px 0; border:0.5px solid rgba(128,128,128,0.2);">
                <div style="font-size: 12px; display: flex; justify-content: space-around;">
                    <span>체감 <b>{feels_like:.1f}°C</b></span>
                    <span>습도 <b>{humidity}%</b></span>
                    <span>풍속 <b>{wind_speed}m/s</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption("날씨 정보를 불러오는 중입니다...")

    st.markdown("---")
    st.caption("⚙️ **서비스 연결 상태**")
    st.caption(f"환율 API: {'🟢 정상 연결' if ENV_EXCHANGERATE_KEY else '🟡 공개 모드'}")
    st.caption(f"날씨 API: {'🟢 정상 연결' if ENV_OPENWEATHER_KEY else '🔴 키 누락'}")

# -------------------------------------------------------------
# 5. 메인 대시보드 (환율 계산기)
# -------------------------------------------------------------
st.title("🧭 글로벌 환율 계산기")
st.caption("한국(KRW), 미국(USD), 일본(JPY), 유럽(EUR), 중국(CNY) 실시간 환율 정보")

# 세션 상태 초기화 (통화 스왑용)
if "from_curr" not in st.session_state:
    st.session_state.from_curr = "KRW"
if "to_curr" not in st.session_state:
    st.session_state.to_curr = "USD"

def swap_currencies():
    temp = st.session_state.from_curr
    st.session_state.from_curr = st.session_state.to_curr
    st.session_state.to_curr = temp

col1, col_swap, col2, col3 = st.columns([3, 1, 3, 3])
curr_list = list(CURRENCY_CITY_MAP.keys())

with col1:
    base_curr = st.selectbox(
        "보유 통화 (From)",
        options=curr_list,
        index=curr_list.index(st.session_state.from_curr),
        key="from_curr",
        format_func=lambda x: f"{CURRENCY_CITY_MAP[x]['flag']} {x} - {CURRENCY_CITY_MAP[x]['name']}"
    )

with col_swap:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    st.button("↔", on_click=swap_currencies, help="두 통화 맞바꾸기", use_container_width=True)

with col2:
    target_curr = st.selectbox(
        "환전할 통화 (To)",
        options=curr_list,
        index=curr_list.index(st.session_state.to_curr),
        key="to_curr",
        format_func=lambda x: f"{CURRENCY_CITY_MAP[x]['flag']} {x} - {CURRENCY_CITY_MAP[x]['name']}"
    )

with col3:
    amount = st.number_input("환전할 금액", min_value=1.0, value=100000.0, step=10000.0, format="%.2f")

# 환율 데이터 조회
rates = get_exchange_rates(base_currency=base_curr, api_key=ENV_EXCHANGERATE_KEY)

if rates and target_curr in rates:
    rate = rates[target_curr]
    converted_amount = amount * rate
    
    st.markdown("---")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.metric(
            label=f"기준 환율 (1 {base_curr})",
            value=f"{rate:,.4f} {target_curr}"
        )
    with m_col2:
        st.metric(
            label="최종 환산 결과",
            value=f"{converted_amount:,.2f} {target_curr}",
            delta=f"{amount:,.2f} {base_curr} 기준"
        )
    with m_col3:
        if base_curr == "JPY" and target_curr == "KRW":
            st.metric("100엔당 원화 환율", f"{rate * 100:,.2f} 원")
        elif base_curr == "KRW" and target_curr == "JPY":
            st.metric("100엔 살 때 필요한 원화", f"{100 / rate:,.2f} 원")
        else:
            inv_rate = 1 / rate if rate != 0 else 0
            st.metric(f"역환율 (1 {target_curr})", f"{inv_rate:,.4f} {base_curr}")

    # -------------------------------------------------------------
    # 6. 여행 & 직구용 퀵 환산표 (Quick Sheet)
    # -------------------------------------------------------------
    st.markdown("### ✈️ 여행 & 직구용 퀵 환산표 (Quick Sheet)")
    st.caption(f"현지에서 자주 쓰이는 대표 금액 단위별 즉시 환산표입니다. ({target_curr} ⇄ {base_curr})")

    if target_curr in ["KRW", "JPY"]:
        units = [100, 500, 1000, 5000, 10000, 50000]
    else:
        units = [1, 5, 10, 20, 50, 100, 500]

    sheet_data_target = []
    inv_rate = 1 / rate if rate != 0 else 0

    for u in units:
        sheet_data_target.append({
            f"현지 금액 ({target_curr})": f"{u:,.0f} {target_curr}",
            f"환산 금액 ({base_curr})": f"{u * inv_rate:,.2f} {base_curr}"
        })

    sheet_col1, sheet_col2 = st.columns(2)

    with sheet_col1:
        st.markdown(f"**📌 {target_curr} → {base_curr} 퀵 환산표**")
        st.dataframe(pd.DataFrame(sheet_data_target), use_container_width=True, hide_index=True)

    with sheet_col2:
        if base_curr in ["KRW", "JPY"]:
            base_units = [1000, 5000, 10000, 50000, 100000, 500000]
        else:
            base_units = [1, 5, 10, 20, 50, 100]

        sheet_data_base = []
        for bu in base_units:
            sheet_data_base.append({
                f"내 금액 ({base_curr})": f"{bu:,.0f} {base_curr}",
                f"환산 수령액 ({target_curr})": f"{bu * rate:,.2f} {target_curr}"
            })
        
        st.markdown(f"**📌 {base_curr} → {target_curr} 퀵 환산표**")
        st.dataframe(pd.DataFrame(sheet_data_base), use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # 7. 타 통화 환산 요약 카드 그리드 (Card Grid)
    # -------------------------------------------------------------
    st.markdown("### 🌐 타 통화 동시 수령액 요약")
    
    other_currs = [c for c in CURRENCY_CITY_MAP.keys() if c != base_curr]
    card_cols = st.columns(len(other_currs))

    for idx, c_code in enumerate(other_currs):
        c_rate = rates.get(c_code, 0)
        c_val = amount * c_rate
        meta = CURRENCY_CITY_MAP[c_code]
        
        with card_cols[idx]:
            st.markdown(f"""
            <div class="metric-card">
                <span style="font-size: 24px;">{meta['flag']}</span>
                <div style="font-size: 13px; color: #888; margin-top: 4px;">{meta['country']} ({c_code})</div>
                <div style="font-size: 17px; font-weight: bold; margin: 6px 0;">{c_val:,.2f} {meta['symbol']}</div>
                <div style="font-size: 11px; color: #aaa;">1 {base_curr} = {c_rate:,.4f}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.error("환율 데이터를 정상적으로 불러올 수 없습니다. 인터넷 상태 및 API 키를 점검해 주세요.")