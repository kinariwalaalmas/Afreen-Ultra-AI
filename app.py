import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio, web_search, get_ai_response
from ui_components import render_plus_menu, render_sidebar, render_quick_actions
from vision_logic import analyze_image
from finance_expert import get_stock_analysis
from phone_control import get_phone_action

# 1. Page Config
st.set_page_config(page_title="Afreen Ultra Pro", layout="wide")
apply_styles()
selected_brain = render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Setup Clients
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("⚠️ Jaan, API Keys in Secrets check kijiye!")
    st.stop()

st.title("👸 Afreen")

# 3. UI Elements
audio_data, photo, ticker = render_plus_menu()
if not st.session_state.messages: render_quick_actions()

user_msg = st.chat_input("Jaan, puchiye...")

# 4. Input Processing
if audio_data: user_msg = transcribe_audio(groq_client, audio_data['bytes'])
if photo:
    res = analyze_image(GEMINI_KEY, photo)
    st.write(res); asyncio.run(generate_voice(res)); play_audio()
if ticker:
    res = get_stock_analysis(gemini_model, ticker)
    st.write(res); asyncio.run(generate_voice(res)); play_audio()

# 5. Core Logic
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)
    
    url, msg = get_phone_action(user_msg)
    if url:
        st.info(msg); st.link_button("Run Action 🚀", url, use_container_width=True)
    else:
        with st.spinner("Thinking..."):
            search = web_search(user_msg) if any(x in user_msg.lower() for x in ["news", "market"]) else ""
            ans = get_ai_response(selected_brain, st.session_state.messages, search)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"): st.write(ans)
            asyncio.run(generate_voice(ans)); play_audio()

# Show History
for m in st.session_state.messages[:-1]:
    with st.chat_message(m["role"]): st.write(m["content"])
