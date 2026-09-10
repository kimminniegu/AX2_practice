# random 모듈을 이용해서 1~45중 중복 없는 번호 6개를 뽑고 
# 자료구조: set, 버튼을 누르면 5개 세트를 한 번에 생성
# datetime 으로 생성 시간도 함께 보여준다.
# 로또 v1
# 로또 v2

from datetime import datetime
import random
import streamlit as st


# 1. 로또 번호 6개 생성 함수
def lotto_set() -> list:
    """1~45에서 중복없이 번호 6개 뽑아 정렬된 리스트로 반환"""
    number = set()

    while len(number) < 6:
        number.add(random.randint(1, 45))

    return sorted(number)


# 2. Streamlit 화면 UI
st.title("🎱 오늘의 로또 번호")
st.caption("버튼을 누르면 1~45 사이의 중복 없는 번호 6개짜리 세트를 5개 생성합니다.")
st.markdown("---")

# 버튼 클릭 조건문
if st.button("🍀 부자 되는 버튼 🍀"):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"⏱️ **생성 시각:** {now_str}")
    st.write("")

    # 5세트 생성 및 숫자 출력
    for set_index in range(1, 6):
        lotto_num = lotto_set()
        # 숫자를 보기 편하게 쉼표로 연결 (예: 3, 12, 23, 31, 38, 42)
        numbers_str = ", ".join(f"{num:02d}" for num in lotto_num)
        st.write(f"**{set_index} 세트 :** {numbers_str}")
else:
    st.info("위 버튼을 눌러 행운의 번호를 받아보세요!")