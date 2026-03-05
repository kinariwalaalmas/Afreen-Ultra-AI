import streamlit as st
import asyncio
from ui_components import render_plus_menu, render_sidebar
from ai_engine import deep_scanner, get_ai_response, generate_voice, play_audio

st.set_page_config(page_title="Afreen Pro", layout="wide")
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []
    # 🎀 Automated "Hey Jaan" Greeting
    welcome = "Hey Jaan! 👸 Afreen aapka intezar kar rahi thi. Bataiye, aaj kiski ID scan karni hai ya Surat market ka kya haal hai?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    asyncio.run(generate_voice(welcome))

st.title("👸 Afreen Pro")
id_input, scan_btn, audio, photo = render_plus_menu()

# Greeting Play on Start
if len(st.session_state.messages) == 1: play_audio()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

user_msg = st.chat_input("Jaan, puchiye...") or (id_input if scan_btn else None)

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)

    with st.spinner("Afreen is scanning the web for you..."):
        context = deep_scanner(user_msg)
        ans = get_ai_response(st.session_state.messages, context)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
        with st.chat_message("assistant"): 
            st.write(ans)
            # 📸 Stock Image logic for Clothes/Trends
            if any(x in user_msg.lower() for x in ["surat", "trend", "cloth", "baggy"]):
                st.image("https://images.unsplash.com/photo-1523381210434-271e8be1f52b?auto=format&fit=crop&w=800", caption="Latest Surat Trends")
        
        asyncio.run(generate_voice(ans))
        play_audio()
