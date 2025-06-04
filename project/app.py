import time
import threading
import streamlit as st

from audio import record_chunk
from transcribe import transcribe_audio
from summarize import summarize
from export import export_txt, export_docx


st.set_page_config(page_title="Interview Assistant", layout="wide")

if 'transcript' not in st.session_state:
    st.session_state['transcript'] = ''
if 'summary' not in st.session_state:
    st.session_state['summary'] = ''
if 'running' not in st.session_state:
    st.session_state['running'] = False
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = 0.0

lang = st.sidebar.selectbox('Language / 언어', ['English', '한국어'])
st.session_state['lang'] = lang

status_placeholder = st.sidebar.empty()
duration_placeholder = st.sidebar.empty()

def run_interview():
    st.session_state['status'] = 'Listening'
    while st.session_state.get('running', False):
        path = record_chunk(duration=5)
        if path:
            text = transcribe_audio(path)
            st.session_state['transcript'] += text + '\n'
            st.session_state['summary'] = summarize(
                st.session_state['transcript'], language=st.session_state['lang']
            )
        else:
            st.session_state['running'] = False
        time.sleep(0.1)
    st.session_state['status'] = 'Idle'

col1, col2 = st.columns(2)

with col1:
    if not st.session_state['running']:
        if st.button('Start Interview' if lang == 'English' else '인터뷰 시작'):
            st.session_state['running'] = True
            st.session_state['start_time'] = time.time()
            thread = threading.Thread(target=run_interview, daemon=True)
            st.session_state['thread'] = thread
            thread.start()
    else:
        if st.button('Stop Interview' if lang == 'English' else '인터뷰 종료'):
            st.session_state['running'] = False

    st.text_area('Transcript' if lang == 'English' else '전사 결과', st.session_state['transcript'], height=300)

with col2:
    st.text_area('Summary' if lang == 'English' else '요약', st.session_state['summary'], height=300)

export_col1, export_col2 = st.columns(2)

with export_col1:
    if st.button('Export TXT' if lang == 'English' else 'TXT 저장'):
        export_txt(st.session_state['summary'], 'summary.txt')
        st.success('Saved as summary.txt' if lang == 'English' else 'summary.txt로 저장되었습니다.')
with export_col2:
    if st.button('Export DOCX' if lang == 'English' else 'DOCX 저장'):
        export_docx(st.session_state['summary'], 'summary.docx')
        st.success('Saved as summary.docx' if lang == 'English' else 'summary.docx로 저장되었습니다.')

status = 'Listening' if st.session_state.get('running') else 'Idle'
if st.session_state.get('lang') == '한국어':
    status = '녹음 중' if st.session_state.get('running') else '대기 중'
status_placeholder.write(f"Status: {status}" if lang == 'English' else f"상태: {status}")

if st.session_state.get('running'):
    elapsed = int(time.time() - st.session_state['start_time'])
    duration_placeholder.write(f"Duration: {elapsed}s" if lang == 'English' else f"경과 시간: {elapsed}초")
else:
    duration_placeholder.write("")
