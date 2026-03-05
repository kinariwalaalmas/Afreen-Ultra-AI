import streamlit as st
import asyncio
from styles import apply_styles
from ui_components import render_plus_menu, render_sidebar
from ai_engine import deep_scanner, get_ai_response, generate_voice, play_audio

st.set_page_config(page_title="Afreen Pro", layout="wide")
apply_styles()
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Hey Jaan! 👸 Afreen haazir hai. Bataiye, aaj kiski ID scan karni hai?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    asyncio.run(generate_voice(welcome))

st.title("👸 Afreen Ultra Pro")
id_url, scan_btn, audio, photo = render_plus_menu()

# Initial Greeting Voice
if len(st.session_state.messages) == 1: play_audio()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

user_input = st.chat_input("Jaan, puchiye...") or (id_url if scan_btn else None)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)

    with st.spinner("Afreen is scanning public records..."):
        context, images = deep_scanner(user_input)
        ans = get_ai_response(st.session_state.messages, context)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
        with st.chat_message("assistant"):
            st.write(ans)
            if images: st.image(images[0], caption=f"Visual for {user_input}")
        
        asyncio.run(generate_voice(ans))
        play_audio()
