import streamlit as st
st.title("간단한 인사")
st.text_input("이름을 입력하세요:", key="name")
if st.button("인사하기"):
    name = st.session_state.name
    if name:
        st.write(f"안녕하세요, {name}님! 반갑습니다!")
#uv run streamlit run test.py

st.sidebar.title("조회 조건")
dept = st.sidebar.selectbox("부서를 선택하세요:", ["전체", "인사팀", "개발팀", "마케팅팀"], key="department")
st.write(f"선택한 부서: {dept}")

if st.button("재미있는 기능"):
    st.balloons()
    st.snow()
    st.balloons()
    st.balloons()
    st.balloons()
    st.balloons()
st.info("이 앱은 Streamlit을 사용하여 간단한 인사와 부서 선택 기능을 제공합니다.")
st.success("성공적으로 실행되었습니다!")
st.warning("주의: 이 앱은 테스트용으로만 사용하세요.")
st.error("오류: 입력값을 확인하세요.")