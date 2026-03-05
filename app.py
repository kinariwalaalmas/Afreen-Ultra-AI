import streamlit as st
import asyncio
from ui_components import render_plus_menu, render_sidebar
from ai_engine import deep_scanner, get_ai_response, generate_voice, play_audio

st.set_page_config(page_title="Afreen Ultra", layout="wide")
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Hey Jaan! 👸 Afreen haazir hai."
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    asyncio.run(generate_voice(welcome))

st.title("👸 Afreen Pro")
id_input, scan_btn, audio, photo = render_plus_menu()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

user_msg = st.chat_input("Jaan, puchiye...") or (id_input if scan_btn else None)

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)

    with st.spinner("Processing..."):
        context = deep_scanner(user_msg) if scan_btn else ""
        ans = get_ai_response(st.session_state.messages, context)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
        asyncio.run(generate_voice(ans))
        play_audio()
