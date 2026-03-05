import streamlit as st
import asyncio
from ui_components import render_plus_menu, render_sidebar
from ai_engine import deep_scanner, get_ai_response, generate_voice, play_audio

st.set_page_config(page_title="Afreen Pro", layout="wide")
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👸 Afreen Ultra")
id_input, scan_btn, audio, photo = render_plus_menu()

user_msg = st.chat_input("Jaan, puchiye...") or (id_input if scan_btn else None)

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)

    with st.spinner("Afreen is digging deep for you..."):
        # Live Web Search
        context = deep_scanner(user_msg)
        
        # AI Response
        ans = get_ai_response(st.session_state.messages, context)
        
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
        
        asyncio.run(generate_voice(ans))
        play_audio()
