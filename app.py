import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio, web_search, get_ai_response
from ui_components import render_plus_menu, render_sidebar, render_quick_actions
from phone_control import get_phone_action

st.set_page_config(page_title="Afreen Pro", layout="wide")
apply_styles()
render_sidebar() # No brain choice variable needed anymore!

if "messages" not in st.session_state:
    st.session_state.messages = []

_, groq_client = get_clients()
if not groq_client:
    st.error("Jaan, Secrets check kijiye!")
    st.stop()

st.title("👸 Afreen")
audio_data, photo, ticker = render_plus_menu()
if not st.session_state.messages: render_quick_actions()

user_msg = st.chat_input("Jaan, puchiye...")

if audio_data: 
    user_msg = transcribe_audio(groq_client, audio_data['bytes'])

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)
    
    url, msg = get_phone_action(user_msg)
    if url:
        st.info(msg); st.link_button("Run Action 🚀", url, use_container_width=True)
    else:
        with st.spinner("Afreen is using her Super-Brain..."):
            search = web_search(user_msg) if any(x in user_msg.lower() for x in ["news", "market"]) else ""
            ans = get_ai_response(st.session_state.messages, search)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"): st.write(ans)
            asyncio.run(generate_voice(ans)); play_audio()

for m in st.session_state.messages[:-1]:
    with st.chat_message(m["role"]): st.write(m["content"])
