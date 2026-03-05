import streamlit as st
import asyncio
from ui_components import render_plus_menu, render_sidebar
from ai_engine import deep_scanner, get_ai_response, generate_voice, play_audio

st.set_page_config(page_title="Afreen Pro", layout="wide")
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []
    # 🎀 Initial Greeting Logic
    welcome_msg = "Hey Jaan! 👸 Afreen haazir hai. Aaj hum Surat market mein kya kamaal karenge?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    asyncio.run(generate_voice(welcome_msg))

st.title("👸 Afreen Pro")
id_input, scan_btn, audio, photo = render_plus_menu()

# Display Welcome/Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

# Logic for Input
user_msg = st.chat_input("Jaan, kuch puchiye...") or (id_input if scan_btn else None)

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)

    with st.spinner("Afreen is scanning the world for you..."):
        context = deep_scanner(user_msg)
        ans = get_ai_response(st.session_state.messages, context)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): 
            st.write(ans)
            # 🖼️ Stock Image functionality (Aesthetic formatting)
            if "Surat" in user_msg: 
                st.image("https://source.unsplash.com/800x400/?fashion,clothes", caption="Latest Trends")
        
        asyncio.run(generate_voice(ans))
        play_audio()
