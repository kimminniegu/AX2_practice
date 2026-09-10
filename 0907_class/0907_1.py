"""
타이타닉 데이터 셋 기초 탐색
pandas head, tail, shape, input, columns 를 사용해서 데이터 셋의 기본 정보를 화면에 순서대로 보여주는 streamlit 앱이다. 
실행 방법: streamlit run 0907_1.py
"""

import pandas as pd
import streamlit as st
import io

# titanic.csv 가져오기
csv_path = 'Titanic.csv'

st.title("🛳️ 타이타닉 데이터셋 기초 탐색")
st.caption("pandas의 head, tail, shape, input, columns로  데이터 셋의 기본 정보를 확인합니다.")

# st.file_uploaderfh 파일을 직접 올릴 수 있다. 아무것도 올리지 않으면 
# 아래의 기존 로직대로 폴더 타이타닉 파일을 그대로 찾아서 읽는다.

upload_file = st.file_uploader('Titanic.csv 파일을 직접 업로드 할 수 있습니다.(선택사항)',type="csv")

# if 조건식:
#     참 일때 결과
# else:
#     거짓일 때 결과
if upload_file is not None :
    df = pd.read_csv(upload_file)
else : 
    try:
        df=pd.read_csv(csv_path)
    except FileNotFoundError:
        # 파일이 없을 때, 사용자가 무엇을 해야 하는지 화면에 안내한다.
        st.error("타이타닉 파일을 찾을 수 없습니다.")
        st.info("같은 경로에 파일을 업로드 하거나 csv 파일을 폴더에 넣고 새로고침 하세요")
        df = None

if df is not None : 
    st.subheader("1) head (): 데이터의 앞 부분 5개 행 미리보기")
    st.dataframe(df.head(), width="stretch") # 기본행 5개 

    st.subheader("2) tail (): 데이터의 뒷 부분 5개 행 미리보기")
    st.dataframe(df.tail(), width="stretch") # 기본행 5개 

    st.subheader("3) shape (): 행 개수, 열 개수")
    col1,col2 = st.columns(2)

    with col1:
        st.metric("행 개수", f"{df.shape[0]}개")
                  
    with col2:
        st.metric("열 개수", f"{df.shape[1]}개")
    st.subheader("4) columns: 전체 열(컬럼) 이름 목록")
    # st.write(df.columns) 표 형태로 보임
    st.write(list(df.columns))
    # st.write(list[int](df.columns)) 대괄호 사이 데이터 형식 지정, 생략 가능

    st.subheader("5) info() : 각 열의 자료형과 결측치(NaN) 여부 요약")
    # df.info(): 값을 리턴하지 않고, 화면에 직접적으로 출력만 해주는 함수라서
    # os.StringIO() 라는 "메모리 위의 가짜 파일"에 결과를 받아낸 뒤, 그 내용을 txt로 보여준다. 

    buffer = io.StringIO()
    df.info(buf= buffer)
    st.text(buffer.getvalue())

# info_df = pd.DataFrame({
#     "타입": df.dtypes,
#     "결측치 아닌 개수": df.notna().sum(),
#     "결측치 개수": df.isna().sum(),
#    })
# st.dataframe(info_df, width="stretch")

    st.success("기초 정보 확인이 끝났습니다.")