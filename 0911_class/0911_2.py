import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="나의 첫번째 챗봇", page_icon="🤖")
st.title("예제 1) 나의 첫번째 챗봇")
st.caption("질문 하나 입력하면 OpenAI chat Completions API를 한 번 호출, 답변을 받아오는 가장 단순한 방법")

# ------------------------사이드바 API 모델---------------------------- 
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API KEY", type="password", help="sk- 로 시작하는 OpenAI API KEY를 넣어주세요")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    st.markdown("[API 발급 받기](https://platform.openai.com/home)")

# -----------------------메인 화면---------------------------------
question = st.text_input("질문을 입력하세요", placeholder="예) 오늘 날씨가 어떤가요?")

if st.button("질문하기",type="primary"):
    if not api_key:
        st.error("OpenAI API Key를 입력하세요.")
    elif not question:
        st.warning("질문을 입력하세요")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            with st.spinner("답변을 생각하는 중..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "당신은 극도로 현실적이고 논리적인(쌉T) 조언자이자 친절한 전문가입니다. 감정에 치우치지 않고 객관적인 사실과 현실적인 해결책을 친절하게 제시하세요."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                )

            # 답변 출력
            answer = response.choices[0].message.content
            st.markdown("### 💬 답변")
            st.write(answer)

            # 토큰 사용량 정보 출력
            usage = response.usage
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("입력 토큰", f"{usage.prompt_tokens}개")
            col2.metric("출력 토큰", f"{usage.completion_tokens}개")
            col3.metric("총 토큰 수", f"{usage.total_tokens}개")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")