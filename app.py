import streamlit as st
import asyncio
from ui_components import render_sidebar
from ai_engine import speech_to_text, get_ai_response, generate_voice, play_audio, get_news_ticker, analyze_image

st.set_page_config(page_title="Afreen Ultra", layout="wide")
render_sidebar()

# 1. News Ticker (Top)
st.markdown(f"**📢 News:** <marquee>{get_news_ticker()}</marquee>", unsafe_allow_html=True)

# 2. Business Planner (Sidebar)
if "tasks" not in st.session_state: st.session_state.tasks = []
with st.sidebar:
    st.write("📋 **Daily Planner**")
    new_task = st.text_input("Add Task")
    if st.button("Add"): st.session_state.tasks.append(new_task)
    for t in st.session_state.tasks: st.checkbox(t)

# 3. Main Chat & Tools
st.title("👸 Afreen Pro 2026")

# Layout: Mic Left, Chat Right
from streamlit_mic_recorder import mic_recorder
col1, col2 = st.columns([1, 6])
with col1:
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='main_mic')
with col2:
    img_file = st.file_uploader("📷 Fashion Scan", type=['jpg', 'png'])
    user_input = st.chat_input("Jaan, puchiye...")

# 🎤 Voice Handling (Mic Fix Solution)
if audio_data and audio_data.get('bytes'):
    with st.spinner("Afreen sun rahi hai..."):
        transcript = speech_to_text(audio_data['bytes'])
        if transcript: user_input = transcript

# 🖼️ Image Recognition Handling
if img_file:
    with st.spinner("Scanning fabric..."):
        ans = analyze_image(img_file)
        st.write(ans)
        asyncio.run(generate_voice(ans)); play_audio()

# ... (Previous Chat Logic) ...
