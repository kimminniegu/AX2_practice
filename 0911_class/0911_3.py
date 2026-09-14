# 대화 기록을 기억하는 멀티턴 챗봇
# st.session_state에 대화 기록을 저장해서, 이전 대화 맥락을 기억하는 챗봇
# st.chat_massage / st.chat_input 같은 Streamlit의 채팅 전용 위젯을 사용합니다
# stream=True 옵션으로 답변이 실시간으로 타이핑되듯 출력됩니다.
# streamlit run 0911_3.py

# 시스템 메시지를 사용자가 설정하도록
# 대화 기록 초기화 버튼

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="멀티턴 챗봇", page_icon="🤖")
st.title("예제 2) 기억하는 멀티턴 챗봇")
st.caption("대화 맥락을 기억하며 실시간 스트리밍으로 답변하는 챗봇입니다.")

# ------------------------사이드바 설정---------------------------- 
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("OpenAI API KEY", type="password", help="sk- 로 시작하는 OpenAI API KEY를 넣어주세요")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    
    st.markdown("---")
    st.subheader("🎭 페르소나 (시스템 프롬프트)")
    default_system_prompt = "당신은 극도로 현실적이고 논리적인(쌉T) 조언자이자 친절한 전문가입니다. 감정에 치우치지 않고 객관적인 사실과 현실적인 해결책을 친절하게 제시하세요."
    system_prompt = st.text_area(
        "챗봇의 성격/역할을 지정하세요",
        value=default_system_prompt,
        height=120
    )
    
    st.markdown("---")
    if st.button("🗑️ 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("[API 발급 받기](https://platform.openai.com/home)")

# -----------------------세션 상태 초기화-------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------기존 대화 렌더링--------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------사용자 입력 및 답변 생성-----------------
if prompt := st.chat_input("메시지를 입력하세요..."):
    if not api_key:
        st.error("먼저 사이드바에 OpenAI API Key를 입력하세요.")
    else:
        # 1. 사용자 입력을 화면에 표시하고 히스토리에 추가
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2. OpenAI API 요청 메시지 구성
        api_messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        # 3. 모델 답변 스트리밍 생성 및 상태 표시
        try:
            client = OpenAI(api_key=api_key)
            with st.chat_message("assistant"):
                # 답변 생성 중 안내 메시지 출력
                status_placeholder = st.empty()
                status_placeholder.markdown("⏳ *답변을 생성하는 중입니다...*")

                stream = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    stream=True
                )
                
                # 첫 토큰이 나오기 시작하면 상태 문구를 지우고 스트리밍 출력
                status_placeholder.empty()
                response = st.write_stream(stream)
            
            # 어시스턴트 답변 히스토리에 추가
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")