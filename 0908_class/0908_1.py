# -*- coding: utf-8 -*-
"""
raw_trade_data.csv 파일 분석 및 시각화 웹 대시보드
- HS code가 85로 시작하는 (반도체류) 품목 필터링
- 국가명: 미국 또는 베트남 필터링
- 수출금액 0보다 큰 수 (실제 수출실적이 있는 데이터) 필터링
- 수출금액 상위 10건 화면 표시 및 report.csv 저장
- Streamlit을 활용한 현대적이고 반응성이 뛰어난 UI 구현
"""
# 수정본
# 또 수정하자
import os
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="반도체류 대미/대베트남 수출실적 분석",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS로 UI 스타일 고도화 (Modern & Alive 느낌 부여)
st.markdown("""
<style>
    /* 전체 배경 및 폰트 미세 조정 */
    .reportview-container {
        background-color: #f8f9fa;
    }
    /* 타이틀 영역 스타일링 */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.8rem;
    }
    /* 카드(Metric) 컴포넌트 세부 스타일링 */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1.2rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    div[data-testid="metric-container"] label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #64748b;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    /* 경고창/성공창 스타일링 */
    .stAlert {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# 1. CSV 파일 경로 탐색
csv_filename = "raw_trade_data.csv"
csv_path = None

# 여러 가능한 위치 탐색 (로컬, 부모 폴더의 common, 정적 절대 경로 등)
possible_paths = [
    csv_filename,
    os.path.join("..", "common", csv_filename),
    os.path.join("C:\\Users\\user\\AX2_practice\\common", csv_filename),
    os.path.join("..", csv_filename)
]

for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if not csv_path:
    st.error(f"❌ '{csv_filename}' 파일을 찾을 수 없습니다. 경로 설정을 확인해주세요.")
    st.stop()

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_and_filter_data(filepath):
    # CSV 로드
    df = pd.read_csv(filepath)
    
    # HS code 문자열 변환 및 필터링 (85로 시작)
    df['hs_code'] = df['hs_code'].astype(str)
    cond_hs = df['hs_code'].str.startswith('85')
    
    # 국가 필터링 (미국 또는 베트남)
    cond_country = df['국가명'].isin(['미국', '베트남'])
    
    # 수출금액 필터링 (0보다 큰 수)
    cond_export = df['수출금액'] > 0
    
    # 다중 조건 필터링 적용
    df_filtered = df[cond_hs & cond_country & cond_export].copy()
    
    # 수출금액 기준 내림차순 정렬 및 상위 10건 추출
    df_top10 = df_filtered.sort_values(by='수출금액', ascending=False).head(10)
    
    return df_filtered, df_top10

try:
    df_filtered, df_top10 = load_and_filter_data(csv_path)
except Exception as e:
    st.error(f"데이터를 처리하는 과정에서 에러가 발생했습니다: {e}")
    st.stop()

# 3. 데이터 저장 (자동 저장)
# 수출금액 상위 10건을 report.csv로 항상 저장합니다.
report_path = "report.csv"
try:
    df_top10.to_csv(report_path, index=False, encoding='utf-8-sig')
    save_success = True
except Exception as e:
    save_success = False
    save_error = e

# 4. Streamlit UI 구성
st.markdown("<div class='main-title'>🚢 반도체류(HS Code 85) 대미/대베트남 수출 실적 분석</div>", unsafe_allow_html=True)
st.write("")

# 소개 및 파일 저장 알림
col_intro, col_save = st.columns([2, 1])
with col_intro:
    st.markdown("""
    이 대시보드는 `raw_trade_data.csv` 파일을 기반으로 **반도체류(HS Code가 85로 시작)** 중 **미국 및 베트남** 대상의 **실제 수출 실적(수출금액 > 0)** 데이터 다중 조건 필터링 결과를 제공합니다.
    """)
with col_save:
    if save_success:
        st.success(f"💾 상위 10건 데이터가 `{report_path}` 파일로 정상 저장되었습니다!")
    else:
        st.error(f"❌ 파일 저장 실패: {save_error}")

# 사이드바 설정 (정보 및 필터 제어)
st.sidebar.header("⚙️ 분석 설정 및 정보")
st.sidebar.markdown(f"**원본 데이터 경로:**\n`{os.path.abspath(csv_path)}`")
st.sidebar.markdown(f"**필터 조건:**\n1. HS Code `85*` (반도체류)\n2. 국가: `미국`, `베트남`\n3. 수출실적 `> 0` USD")

# 대화형 사이드바 추가 컨트롤 (기본값 설정 유지하면서 다양성 추가)
show_all_filtered = st.sidebar.checkbox("조건을 충족하는 전체 필터링 데이터 보기", value=False)

# KPI 대시보드 메트릭 영역
st.write("### 📊 주요 실적 지표 (Key Metrics)")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

total_filtered_count = len(df_filtered)
top10_total_amount = df_top10['수출금액'].sum()
top10_avg_amount = df_top10['수출금액'].mean()
max_export_amount = df_top10['수출금액'].max()

with m_col1:
    st.metric(label="필터 조건 부합 총 건수", value=f"{total_filtered_count:,} 건")
with m_col2:
    st.metric(label="상위 10건 총 수출액", value=f"${top10_total_amount:,.0f}")
with m_col3:
    st.metric(label="상위 10건 평균 수출액", value=f"${top10_avg_amount:,.0f}")
with m_col4:
    st.metric(label="최고 단일 수출액", value=f"${max_export_amount:,.0f}")

st.write("")

# 데이터 테이블 및 차트 배치
tab1, tab2 = st.tabs(["📋 상위 10건 데이터", "📈 시각화 분석"])

with tab1:
    st.markdown("#### 🏆 수출금액 기준 상위 10건 상세 내역")
    # 인덱스를 1부터 시작하도록 설정
    df_display = df_top10.copy()
    df_display.index = range(1, len(df_display) + 1)
    
    # 이쁘게 표로 출력
    st.dataframe(df_display, width='stretch')
    
    # 다운로드 버튼 제공
    csv_bytes = df_top10.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button(
        label="📥 CSV 파일 다운로드 (report.csv)",
        data=csv_bytes,
        file_name='report.csv',
        mime='text/csv'
    )

with tab2:
    st.markdown("#### 📊 상위 10건 수출액 분포 및 추이")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**1. 날짜별 수출 실적 추이**")
        # 날짜와 국가별로 그룹화된 상위 10건 차트화용 데이터
        chart_data_time = df_top10.sort_values(by='날짜')
        st.bar_chart(
            data=chart_data_time,
            x='날짜',
            y='수출금액',
            color='국가명',
            width='stretch'
        )
        
    with chart_col2:
        st.markdown("**2. 국가별 수출 총합 비교 (상위 10건 기준)**")
        country_group = df_top10.groupby('국가명')['수출금액'].sum().reset_index()
        st.bar_chart(
            data=country_group,
            x='국가명',
            y='수출금액',
            width='stretch'
        )

# 추가 정보 섹션
if show_all_filtered:
    st.write("---")
    st.write(f"### 🔍 조건 부합 전체 데이터 ({total_filtered_count}건)")
    st.dataframe(df_filtered.sort_values(by='날짜', ascending=False), width='stretch')
