from datetime import datetime, timedelta
import random
import streamlit as st


# 1. 로또 번호 6개 생성 함수
def lotto_set() -> list:
    """1~45에서 중복없이 번호 6개 뽑아 정렬된 리스트로 반환"""
    number = set()
    while len(number) < 6:
        number.add(random.randint(1, 45))
    return sorted(number)


# 2. 세션 상태(누적 기록 저장소) 초기화
if "lotto_history" not in st.session_state:
    st.session_state.lotto_history = []

# 3. 24시간 지난 기록 자동 삭제 (필터링)
now = datetime.now()
st.session_state.lotto_history = [
    item
    for item in st.session_state.lotto_history
    if now - item["created_at"] < timedelta(hours=24)
]

# 4. Streamlit 화면 UI
st.title("🎱 오늘의 로또 번호")
st.caption(
    "버튼을 누르면 5세트가 생성되어 아래에 누적됩니다. (생성 후 24시간이 지난 기록은 자동 삭제)"
)
st.markdown("---")

# 버튼 클릭 시 새로운 세트 생성 및 세션에 누적 저장
if st.button("🍀 부자 되는 버튼 🍀"):
    # 5세트 생성
    new_sets = [lotto_set() for _ in range(5)]

    # 현재 시각(datetime 객체 및 문자열)과 함께 저장
    history_entry = {
        "created_at": now,
        "time_str": now.strftime("%Y-%m-%d %H:%M:%S"),
        "sets": new_sets,
    }

    # 최신 기록이 맨 위로 오도록 앞에 추가 (뒤에 추가하려면 .append())
    st.session_state.lotto_history.insert(0, history_entry)

# 5. 누적된 기록 화면에 출력 (구분선 포함)
if st.session_state.lotto_history:
    st.write(
        f"### 📋 생성 기록 (총 {len(st.session_state.lotto_history)}회차)"
    )

    for record in st.session_state.lotto_history:
        st.write(f"⏱️ **생성 시각:** {record['time_str']}")

        for idx, lotto_num in enumerate(record["sets"], start=1):
            numbers_str = ", ".join(f"{num:02d}" for num in lotto_num)
            st.write(f"**{idx} 세트 :** {numbers_str}")

        # 회차별 구분선
        st.markdown("---")
else:
    st.info("버튼을 눌러 행운의 번호를 생성해보세요!")