import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="시각 단순 선택주의력 검사", layout="centered")

# 세션 상태 초기화
if 'current' not in st.session_state:
    st.session_state.current = 0
if 'results' not in st.session_state:
    st.session_state.results = []
if 'reaction_times' not in st.session_state:
    st.session_state.reaction_times = []
if 'omission' not in st.session_state:
    st.session_state.omission = 0
if 'commission' not in st.session_state:
    st.session_state.commission = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'shape' not in st.session_state:
    st.session_state.shape = None

shapes = ['원', '세모', '네모']
total_trials = 10
interval = 2

st.title("시각 단순 선택주의력 검사")
st.write("도형이 화면에 나타납니다. **'원'이 보이면 S 키를 입력하고 엔터!**")

# 검사 시작
if st.session_state.current == 0:
    if st.button("검사 시작"):
        st.session_state.current = 1
        st.rerun()
        st.stop()  # rerun 이후 코드 실행 방지

# 검사 진행
elif st.session_state.current <= total_trials:
    placeholder = st.empty()

    if st.session_state.start_time is None:
        st.session_state.shape = random.choice(shapes)
        placeholder.markdown(f"<h1 style='text-align: center;'>{st.session_state.shape}</h1>", unsafe_allow_html=True)
        st.session_state.start_time = time.time()

    response = st.text_input("※ 's'를 입력하고 Enter 키를 누르세요 (2초 안에)", key=f"input_{st.session_state.current}")

    if response:
        rt = time.time() - st.session_state.start_time
        shape = st.session_state.shape
        response = response.strip().lower()

        if shape == '원':
            if response == 's' and rt <= interval:
                st.session_state.reaction_times.append(rt)
                st.session_state.results.append((shape, '정확'))
            else:
                st.session_state.omission += 1
                st.session_state.results.append((shape, 'Omission'))
        else:
            if response == 's':
                st.session_state.commission += 1
                st.session_state.results.append((shape, 'Commission'))
            else:
                st.session_state.results.append((shape, '정상'))

        st.session_state.current += 1
        st.session_state.start_time = None
        st.rerun()

# 결과 출력
else:
    st.subheader("검사 결과")
    if st.session_state.reaction_times:
        avg_rt = sum(st.session_state.reaction_times) / len(st.session_state.reaction_times)
        st.write(f"평균 반응 시간: {avg_rt:.2f}초")
    else:
        st.write("정확한 반응이 없습니다.")

    st.write(f"Omission 오류 수: {st.session_state.omission}")
    st.write(f"Commission 오류 수: {st.session_state.commission}")

    df = pd.DataFrame(st.session_state.results, columns=["자극 도형", "응답 결과"])
    st.dataframe(df)

    if st.button("다시 검사하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
