import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, web_search, get_ai_response
from ui_components import render_plus_menu, render_sidebar, render_quick_actions

st.set_page_config(page_title="Afreen Ultra Pro", layout="wide")
apply_styles()
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👸 Afreen Ultra")
audio_data, photo, ticker = render_plus_menu()

# 1. Agar koi sawal pucha jaye
user_msg = st.chat_input("Jaan, Surat market ke bare mein kuch puchiye...")

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)

    with st.spinner("Afreen is scanning the web and thinking..."):
        # A. Live Search (DuckDuckGo) for News/Market
        context = ""
        if any(x in user_msg.lower() for x in ["news", "market", "surat", "price", "trend"]):
            context = web_search(user_msg)
        
        # B. Get Triple-Brain Response
        ans = get_ai_response(st.session_state.messages, context)
        
        # C. Output
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
            if context: 
                with st.expander("Live Sources 📚"): st.write(context)
        
        asyncio.run(generate_voice(ans))
        play_audio()

# Chat History Display
for m in st.session_state.messages[:-1]:
    with st.chat_message(m["role"]): st.write(m["content"])
