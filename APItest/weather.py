# 날씨 API 실습
# openweathermap 현재 날씨 API로 특정 지역의 날씨를 가져와 출력한다. 
# 사전 준비: API (회원가입 후 발급)
# 외부에 만들어 놓은 env(환경변수)
# pip install requests python-dotenv 
# .env 파일 생성 후, 이곳에 변수명은 OPENWEATHER_API_KEY=발급받은키
# .env.example 파일 안에, OPENWEATHER_API_KEY=your_key > git 에 올라가도 됨
# .env.example 받아서 .env로 이름 바꾸고 자기 API를 채운다

import os
import requests
import pandas as pd
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# .env 경로 지정 및 로드
CURRENT_DIR = Path(__file__).resolve().parent
ENV_PATH = CURRENT_DIR.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 페이지 기본 설정
st.set_page_config(
    page_title="SkyCast | 날씨 대시보드",
    page_icon="🌤️",
    layout="centered"
)

# 날씨 상태별 배경 그라디언트 설정
THEMES = {
    "Clear": "linear-gradient(135deg, #fceabb 0%, #f8b500 100%)",       # 맑음
    "Clouds": "linear-gradient(135deg, #757F9A 0%, #D7DDE8 100%)",      # 구름
    "Rain": "linear-gradient(135deg, #4b6cb7 0%, #182848 100%)",        # 비
    "Snow": "linear-gradient(135deg, #83a4d4 0%, #b6fbff 100%)",        # 눈
    "Thunderstorm": "linear-gradient(135deg, #141E30 0%, #243B55 100%)", # 뇌우
    "Default": "linear-gradient(135deg, #667db6 0%, #0082c8 100%)"
}

def apply_custom_css(theme_gradient):
    st.markdown(f"""
        <style>
        .stApp {{
            background: {theme_gradient};
            background-attachment: fixed;
            color: #ffffff;
        }}
        .weather-card {{
            background: rgba(255, 255, 255, 0.22);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 20px;
            text-align: center;
        }}
        .info-box {{
            background: rgba(255, 255, 255, 0.18);
            border-radius: 14px;
            padding: 16px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(6px);
        }}
        .chart-box {{
            background: rgba(255, 255, 255, 0.18);
            border-radius: 18px;
            padding: 20px;
            margin-top: 20px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
        }}
        .temp-display {{
            font-size: 3.8rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 10px 0;
        }}
        .sub-text {{
            font-size: 0.95rem;
            opacity: 0.9;
        }}
        </style>
    """, unsafe_allow_html=True)

# 헤더 타이틀
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🌦️ SkyCast Weather</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.85; margin-bottom: 25px;'>실시간 날씨 & 기온 예보 대시보드</p>", unsafe_allow_html=True)

# 검색 바
city = st.text_input("도시 검색", value="Seoul", placeholder="도시명을 영어로 입력하세요 (예: Seoul, Tokyo, London)")

if not API_KEY:
    st.error("`.env` 파일에 `OPENWEATHER_API_KEY`를 설정해주세요.")
    st.stop()

if city:
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=kr"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=kr"
    
    try:
        cur_res = requests.get(current_url)
        forecast_res = requests.get(forecast_url)
        
        cur_data = cur_res.json()
        forecast_data = forecast_res.json()

        if cur_res.status_code == 200:
            weather_main = cur_data["weather"][0]["main"]
            weather_desc = cur_data["weather"][0]["description"]
            # 어색한 번역을 자연스러운 한국어로 매핑하는 예시
            weather_kr_map = {
                "온흐림": "흐림 (하늘 뒤덮임)",
                "튼구름": "구름 많음",
                "실비": "이슬비",
                "약한 비": "가벼운 비"
            }

            # 변환 적용
            weather_desc = weather_kr_map.get(weather_desc, weather_desc)
            icon_code = cur_data["weather"][0]["icon"]
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
            
            temp = round(cur_data["main"]["temp"], 1)
            feels_like = round(cur_data["main"]["feels_like"], 1)
            humidity = cur_data["main"]["humidity"]
            wind_speed = cur_data["wind"]["speed"]
            pressure = cur_data["main"]["pressure"]
            city_name = cur_data["name"]
            country = cur_data["sys"]["country"]

            # 배경 테마 적용
            gradient = THEMES.get(weather_main, THEMES["Default"])
            apply_custom_css(gradient)

            # [1] 현재 날씨 카드
            st.markdown(f"""
                <div class="weather-card">
                    <h2 style="margin: 0;">{city_name}, {country}</h2>
                    <img src="{icon_url}" width="110" style="margin-top: -10px; margin-bottom: -10px;">
                    <div class="temp-display">{temp}°C</div>
                    <p style="font-size: 1.3rem; font-weight: 600; margin: 4px 0;">{weather_desc.capitalize()}</p>
                    <p class="sub-text">체감 온도 {feels_like}°C</p>
                </div>
            """, unsafe_allow_html=True)

            # [2] 상세 정보 그리드 (반응형 3열)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="info-box">
                        <div class="sub-text">💧 습도</div>
                        <h3 style="margin: 6px 0;">{humidity}%</h3>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="info-box">
                        <div class="sub-text">💨 풍속</div>
                        <h3 style="margin: 6px 0;">{wind_speed} m/s</h3>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="info-box">
                        <div class="sub-text">🧭 기압</div>
                        <h3 style="margin: 6px 0;">{pressure} hPa</h3>
                    </div>
                """, unsafe_allow_html=True)

            # [3] 5일 예보 꺾은선 차트 (시간 축 보정)
            if forecast_res.status_code == 200:
                forecast_list = forecast_data.get("list", [])
                
                chart_records = []
                for item in forecast_list:
                    chart_records.append({
                        "시간": item["dt_txt"], # UTC 일시
                        "기온 (°C)": item["main"]["temp"]
                    })

                df = pd.DataFrame(chart_records)
                # 1) 문자열을 datetime 객체로 변환
                df["시간"] = pd.to_datetime(df["시간"])
                # 2) 한국 표준시 (KST = UTC + 9)로 변환
                df["시간"] = df["시간"] + pd.Timedelta(hours=9)
                df = df.set_index("시간")

                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("📈 향후 5일간 기온 추이 (한국 시간 기준)")
                
                # DatetimeIndex를 넣으면 Streamlit이 X축 눈금을 자동으로 깔끔하게 축약 표시합니다.
                st.line_chart(df)

        elif cur_res.status_code == 404:
            st.warning("도시를 찾을 수 없습니다. 철자를 확인해주세요.")
        else:
            st.error(f"데이터 조회 실패: {cur_data.get('message')}")

    except requests.exceptions.RequestException as e:
        st.error(f"통신 에러: {e}")

# --- 환율 API 연동 코드 ---

# 1. 상위 폴더(AX2_practice)의 .env 파일 경로 지정 및 환경변수 로드
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

# 2. API 키 가져오기
api_key = os.getenv("EXCHANGERATE_API_KEY")

# 3. Streamlit 화면 UI 및 API 호출
st.title("💱 실시간 환율 조회 (ExchangeRate-API)")

if not api_key:
    st.error(".env 파일에서 EXCHANGERATE_API_KEY를 찾을 수 없습니다.")
else:
    # 기준 통화 설정 (기본값: USD)
    base_currency = st.selectbox("기준 통화를 선택하세요", ["USD", "KRW", "EUR", "JPY"], index=0)
    
    # ExchangeRate-API 호출 엔드포인트
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get("result") == "success":
            rates = data.get("conversion_rates", {})
            
            # 주요 통화 데이터 추출
            target_currencies = ["KRW", "USD", "EUR", "JPY", "CNY", "GBP"]
            filtered_rates = {k: v for k, v in rates.items() if k in target_currencies}
            
            # DataFrame 변환 후 화면 출력
            df = pd.DataFrame(list(filtered_rates.items()), columns=["통화", f"환율 (1 {base_currency} 기준)"])
            
            st.subheader(f"기준: 1 {base_currency}")
            st.dataframe(df, use_container_width=True)
            
            # 원화(KRW) 환율 카드 표시 (USD 기준일 때)
            if base_currency == "USD" and "KRW" in rates:
                st.metric(label="USD/KRW 환율", value=f"{rates['KRW']:,} 원")
        else:
            st.error(f"API 오류: {data.get('error-type')}")
    else:
        st.error(f"요청 실패 (상태 코드: {response.status_code})")