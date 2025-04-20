import streamlit as st
import random
import time
import pandas as pd

# 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 'start'  # start, show_shape, get_input, done
if 'trial' not in st.session_state:
    st.session_state.trial = 0
if 'shape' not in st.session_state:
    st.session_state.shape = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'results' not in st.session_state:
    st.session_state.results = []
if 'reaction_times' not in st.session_state:
    st.session_state.reaction_times = []
if 'omission' not in st.session_state:
    st.session_state.omission = 0
if 'commission' not in st.session_state:
    st.session_state.commission = 0

shapes = ['원', '세모', '네모']
total_trials = 10

st.set_page_config(page_title="주의력 검사", layout="centered")
st.title("시각 단순 선택주의력 검사")
st.write("도형이 나타납니다. '원'이 보이면 s 키를 입력하고 엔터를 눌러주세요!")

# 단계: 시작
if st.session_state.step == 'start':
    if st.button("검사 시작"):
        st.session_state.step = 'show_shape'
        st.rerun()

# 단계: 도형 보여주기
elif st.session_state.step == 'show_shape':
    st.session_state.shape = random.choice(shapes)
    st.session_state.start_time = time.time()
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.shape}</h1>", unsafe_allow_html=True)
    if st.button("다음"):
        st.session_state.step = 'get_input'
        st.rerun()

# 단계: 입력받기
elif st.session_state.step == 'get_input':
    shape = st.session_state.shape
    start = st.session_state.start_time
    response = st.text_input("※ 's'를 입력하고 Enter 키를 누르세요", key=f"input_{st.session_state.trial}")

    if response:
        rt = time.time() - start
        response = response.strip().lower()

        if shape == '원':
            if response == 's':
                st.session_state.reaction_times.append(rt)
                st.session_state.results.append((shape, '정확', rt))
            else:
                st.session_state.omission += 1
                st.session_state.results.append((shape, 'Omission', None))
        else:
            if response == 's':
                st.session_state.commission += 1
                st.session_state.results.append((shape, 'Commission', None))
            else:
                st.session_state.results.append((shape, '정상', None))

        st.session_state.trial += 1

        if st.session_state.trial >= total_trials:
            st.session_state.step = 'done'
        else:
            st.session_state.step = 'show_shape'
        st.rerun()

# 결과 출력
elif st.session_state.step == 'done':
    st.subheader("검사 결과")
    if st.session_state.reaction_times:
        avg_rt = sum(st.session_state.reaction_times) / len(st.session_state.reaction_times)
        st.write(f"평균 반응 시간: {avg_rt:.2f}초")
    else:
        st.write("정확한 반응이 없습니다.")
    st.write(f"Omission 오류 수: {st.session_state.omission}")
    st.write(f"Commission 오류 수: {st.session_state.commission}")

    df = pd.DataFrame(st.session_state.results, columns=["자극 도형", "응답 결과", "반응 시간"])
    st.dataframe(df)

    if st.button("다시 검사하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
