import streamlit as st
import time
import random

st.set_page_config(page_title="주의력 검사", page_icon="👁️", layout="centered")

st.title("시각 단순 선택주의력 검사")
st.write("도형이 화면에 나타납니다. **'원'이 보이면 S 키를 입력하고 엔터!**")

shapes = ['원', '사각형', '삼각형']
stimuli_count = 30
interval = 2.0

if 'current' not in st.session_state:
    st.session_state.current = 0
    st.session_state.reaction_times = []
    st.session_state.omission = 0
    st.session_state.commission = 0
    st.session_state.results = []

placeholder = st.empty()

start = st.button("검사 시작")

if start:
    st.session_state.current = 0
    st.session_state.reaction_times = []
    st.session_state.omission = 0
    st.session_state.commission = 0
    st.session_state.results = []
    st.experimental_rerun()

if st.session_state.current < stimuli_count and start is False:
    st.write("검사를 시작하려면 위 버튼을 누르세요.")

elif st.session_state.current < stimuli_count:
    shape = random.choice(shapes)
    placeholder.markdown(f"<h1 style='text-align: center;'>{shape}</h1>", unsafe_allow_html=True)

    start_time = time.time()
    response = st.text_input("※ 's'를 입력하고 Enter 키를 누르세요 (2초 안에)", key=str(st.session_state.current))
    end_time = time.time()

    rt = end_time - start_time

    if shape == '원':
        if response.strip().lower() == 's' and rt <= interval:
            st.session_state.reaction_times.append(rt)
            st.session_state.results.append((shape, '정확'))
        else:
            st.session_state.omission += 1
            st.session_state.results.append((shape, 'Omission'))
    else:
        if response.strip().lower() == 's':
            st.session_state.commission += 1
            st.session_state.results.append((shape, 'Commission'))
        else:
            st.session_state.results.append((shape, '정상'))

    time.sleep(interval)
    st.session_state.current += 1
    st.experimental_rerun()

elif st.session_state.current >= stimuli_count:
    placeholder.markdown("### 검사 종료!")
    st.success("결과 요약")
    st.write(f"- 자극 수: {stimuli_count}")
    st.write(f"- 평균 반응 시간: {sum(st.session_state.reaction_times)/len(st.session_state.reaction_times):.3f}초" if st.session_state.reaction_times else "- 반응 없음")
    st.write(f"- 반응 시간 표준편차: {(sum((x - sum(st.session_state.reaction_times)/len(st.session_state.reaction_times))**2 for x in st.session_state.reaction_times)/len(st.session_state.reaction_times))**0.5:.3f}초" if st.session_state.reaction_times else "- 계산 불가")
    st.write(f"- Omission Errors (누락): {st.session_state.omission}")
    st.write(f"- Commission Errors (오경보): {st.session_state.commission}")
