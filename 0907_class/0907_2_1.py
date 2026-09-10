import pandas as pd
import streamlit as st
import io
import os

csv_path = os.path.join(os.path.dirname(__file__), "..","common","superstore_data.csv")

st.title("마케팅 반응 예측치의 결측치 정리")
st.caption("결측치를 제거해 새 csv로 저장합니다.")

try :
    df = pd.read_csv(csv_path)
    
except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다.")

else: 
    st.metric("원본 데이터 행 개수",f"{len(df)}행")

    st.markdown("---")

    st.subheader("1) Income 결측치 처리")
    missing_income_count = df["Income"].isna().sum()
st.write(f"Income 열의 결측치 개수: **{missing_income_count}개**")

# 2. 결측치 제거
df_clean = df.dropna(subset=["Income"])

# 3. 제거 전/후 행 개수 비교 메트릭
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("제거 전", f"{len(df)}행")
with col2:
    st.metric("제거 후", f"{len(df_clean)}행")
with col3:
    st.metric(
        "제거된 행", f"{missing_income_count}행", delta=f"-{missing_income_count}"
    )

st.caption("결측치 24개가 제거된 데이터프레임을 생성했습니다.")

