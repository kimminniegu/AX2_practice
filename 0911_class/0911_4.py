import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="문서 요약 봇", page_icon="📄")
st.title("📄 문서 자동 요약 봇")
st.caption("텍스트/CSV 문서를 업로드하고 옵션을 설정한 뒤 요약 결과를 확인해보세요.")

# ------------------------사이드바 설정---------------------------- 
with st.sidebar:
    st.header("⚙️ 기본 설정")
    api_key = st.text_input("OpenAI API KEY", type="password", help="sk- 로 시작하는 OpenAI API KEY를 넣어주세요")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    
    st.markdown("---")
    st.header("📑 요약 옵션")
    summary_length = st.radio(
        "요약 길이 선택",
        ["짧게 (핵심 3~5줄)", "보통 (주요 내용 요약)", "자세히 (세부 항목 및 데이터 포함)"],
        index=1
    )
    
    summary_style = st.selectbox(
        "요약 스타일 선택",
        [
            "개조식 (불릿 포인트로 핵심 요약)",
            "보고서 형식 (서론-본론-결론 구조)",
            "친절하고 쉬운 설명체 (대화형)",
            "실행 중심 (Action Item 위주 정리)"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("[API 발급 받기](https://platform.openai.com/home)")

# -----------------------메인 화면: 파일 업로드---------------------
uploaded_file = st.file_uploader(
    "요약할 문서를 업로드하세요 (TXT, MD, CSV)",
    type=["txt", "md", "csv"],
    help="텍스트, 마크다운, CSV 파일을 지원합니다."
)

file_text = ""
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            file_text = f"파일명: {uploaded_file.name}\n\n데이터 샘플:\n{df.head(50).to_markdown(index=False)}"
            with st.expander("📊 업로드된 CSV 데이터 미리보기 (상위 5행)"):
                st.dataframe(df.head(5))
        else:
            file_text = uploaded_file.read().decode("utf-8", errors="replace")
            with st.expander("📄 업로드된 문서 내용 미리보기"):
                st.text(file_text[:1000] + ("..." if len(file_text) > 1000 else ""))
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

# -----------------------요약 실행 버튼----------------------------
if st.button("✨ 문서 요약하기", type="primary"):
    if not api_key:
        st.error("사이드바에 OpenAI API Key를 입력하세요.")
    elif not uploaded_file or not file_text:
        st.warning("먼저 요약할 파일을 업로드하세요.")
    else:
        system_prompt = f"""당신은 전문 문서 요약 AI입니다.
사용자가 제공한 문서의 핵심 내용을 다음 조건에 맞춰 정확하게 요약하세요.

[요약 조건]
1. 요약 길이: {summary_length}
2. 요약 스타일: {summary_style}
3. 원문의 중요한 정보와 수치를 왜곡하지 말고 명확하게 정리하세요.
"""
        user_prompt = f"다음 문서를 요약해줘:\n\n{file_text}"

        try:
            client = OpenAI(api_key=api_key)
            
            st.markdown("### 📋 요약 결과")
            status_placeholder = st.empty()
            status_placeholder.markdown("⏳ *문서를 분석하고 요약을 생성하는 중입니다...*")

            # 스트리밍 응답 생성
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True
            )

            status_placeholder.empty()
            st.write_stream(stream)

        except Exception as e:
            st.error(f"요약 중 오류가 발생했습니다: {e}")