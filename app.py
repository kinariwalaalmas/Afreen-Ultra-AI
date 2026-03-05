import streamlit as st
import asyncio
from ui_components import render_plus_menu, render_sidebar
from ai_engine import osint_scanner, get_ai_response, generate_voice, play_audio

st.set_page_config(page_title="Afreen Ultra", layout="wide")
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👸 Afreen Pro")
id_input, scan_btn, audio, photo = render_plus_menu()

# Agar user ne Scanner use kiya
if scan_btn and id_input:
    with st.spinner(f"Searching for {id_input} across the web..."):
        data = osint_scanner(id_input)
        ans = get_ai_response([{"role": "user", "content": f"Tell me about {id_input}"}], data)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
        asyncio.run(generate_voice(ans)); play_audio()

# Normal Chat Logic
user_msg = st.chat_input("Jaan, puchiye...")
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)
    
    # Auto-detect if user is asking for ID or number
    is_id = any(x in user_msg.lower() for x in ["@", "number", "id", "insta", "snap"])
    context = osint_scanner(user_msg) if is_id else ""
    
    ans = get_ai_response(st.session_state.messages, context)
    st.session_state.messages.append({"role": "assistant", "content": ans})
    with st.chat_message("assistant"): st.write(ans)
    asyncio.run(generate_voice(ans)); play_audio()
