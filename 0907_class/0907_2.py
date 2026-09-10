import pandas as pd
import streamlit as st
import io
import os

csv_path = os.path.join(os.path.dirname(__file__), "..","common","superstore_data.csv")

st.title("📋마케팅 반응 예측")
st.caption("pandas의 head, tail, shape, input, columns로  데이터 셋의 기본 정보를 확인합니다.")

upload_file = st.file_uploader('Store.csv 파일을 직접 업로드 할 수 있습니다.(선택사항)',type="csv")

if upload_file is not None :
    df = pd.read_csv(upload_file)
else : 
    try:
        df=pd.read_csv(csv_path)
    except FileNotFoundError:
        # 파일이 없을 때, 사용자가 무엇을 해야 하는지 화면에 안내한다.
        st.error("마케팅 파일을 찾을 수 없습니다.")
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
    st.write(list(df.columns))

    st.subheader("5) info() : 각 열의 자료형과 결측치(NaN) 여부 요약")
    buffer = io.StringIO()
    df.info(buf= buffer)
    st.text(buffer.getvalue())

    st.success("기초 정보 확인이 끝났습니다.")