import streamlit as st
import asyncio
from ui_components import render_plus_menu, render_sidebar
from ai_engine import deep_scanner, get_ai_response, generate_voice, play_audio

st.set_page_config(page_title="Afreen Ultra", layout="wide")
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Hey Jaan! 👸 Afreen aapka intezar kar rahi thi. Bataiye, aaj kiski ID scan karni hai?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    # Initial Voice Greeting
    asyncio.run(generate_voice(welcome))

st.title("👸 Afreen Detective Mode")
id_input, scan_btn, audio, photo = render_plus_menu()

# Greeting Play
if len(st.session_state.messages) == 1: play_audio()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

user_input = st.chat_input("Jaan, puchiye...") or (id_input if scan_btn else None)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)

    with st.spinner("Afreen is scanning public records..."):
        # Scanning logic
        context, images = deep_scanner(user_input)
        ans = get_ai_response(st.session_state.messages, context)
        
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
            # Display Image if found
            if images:
                st.image(images[0], caption=f"Public Visual for {user_input}", use_container_width=True)
            elif "@" in user_input:
                st.info("Jaan, ye account private hai, isliye photos nahi dikh rahi hain. Par maine bio nikaal li hai!")

        asyncio.run(generate_voice(ans))
        play_audio()
