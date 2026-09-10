# 인코딩 자동 감지 + 한글 폰트 막대그래프
# 여러 인코딩 방법("utf-8_sig", "cp949", "euc-kr") 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어야 함
# 객실 등급별 생존율 막대 그래프 생성 후 그림으로 저장 (파일명.png)
# streamlit run 파일명.py

import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager

st.title("인코딩 자동 감지 + 한글 폰트 막대 그래프(타이타닉 연습)")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 열고, 객실등급별 생존율을 그래프로 그립니다.")

csv_path = os.path.join(os.path.dirname(__file__),"titanic_cleaned.csv")
font_path = os.path.join(os.path.dirname(__file__),"에이투지체-4Regular.otf") # 절대 주소/ 실행되는 파일 기준으로 common 파일 찾아감

def read_csv_with_auto_encoding(file_path: str, **kwargs) -> pd.DataFrame:
    """지정된 인코딩 목록('utf-8-sig', 'cp949', 'euc-kr') 순서대로

    CSV 파일을 읽어오는 함수입니다.
    """
    encodings = ["utf-8-sig", "cp949", "euc-kr"]

    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc, **kwargs)
            print(f"성공적으로 읽었습니다. (적용된 인코딩: {enc})")
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue

    raise ValueError(
        f"파일을 읽는 데 실패했습니다. 지원된 모든 인코딩({encodings})이 유효하지 않습니다."
    )

# 인코딩 자동 감지로 csv 읽기,


st.subheader("1) 인코딩 자동 감지")
df = read_csv_with_auto_encoding(csv_path)

st.markdown("---")
# 객실 등급 (Pclass) 별 생존율 집계
# survived 사망 = 0, 생존 = 1 로 표시하는 등급별 평균을 내면 그대로가 등급의 생존비율이다. 
# 전체인원 1000 : 생존 300/ 생존 700

pclass_survival_rate = df.groupby("Pclass")["Survived"].mean().sort_index()
# 먼저 1-3까지 정렬해두고, 부분합을 진행해야 한다!!!!!! 

st.dataframe((pclass_survival_rate * 100).round(1).rename("생존율(%)"))

# df_df = st.dataframe((pclass_survival_rate * 100).round(1).rename("생존율(%)"))
# st.write(df_df) >> 눈으로 확인하고 싶어서 그런것임

# 차트 그리기

st.markdown("---")
st.subheader("3) 객실등급별 생존율 막대그래프")

try: 
    # 폰트 파일이 없으면, FileNotFoundError 발생
    font_prop = font_manager.FontProperties(fname=font_path)
    # matplotlib에서 font_manager에 폰트를 등록하고, 전역 폰트로 설정
    font_manager.fontManager.addfont(font_path) 
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    st.write("에이투지체 폰트를 적용했습니다.")
except FileNotFoundError: 
    st.warning("폰트파일을 찾을 수 없습니다.")

fig, ax = plt.subplots(figsize=(8,5))
(pclass_survival_rate*100).plot(kind='bar',color="blue",ax=ax)
ax.set_title("객실 등급별 생존율")
ax.set_xlabel("객실등급(pclass)")
ax.set_ylabel("생존율(%)")

st.pyplot(fig)

output_png = os.path.join(os.path.dirname(__file__),"chart.png")
fig.savefig(output_png)
st.success