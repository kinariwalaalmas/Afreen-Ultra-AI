import streamlit as st
import asyncio
from ui_power import apply_ui_power
from ai_power import ai_brain, visual_scanner
from system_power import keep_alive_power, voice_power, audio_player

# 1. Activation
st.set_page_config(page_title="Afreen Ultra", layout="wide")
apply_ui_power()
keep_alive_power()

# 2. Greeting
if "messages" not in st.session_state:
    st.session_state.messages = []
    greet = "Hey, main Afreen hoon Jaan, aap kaise hain?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

# 3. UI Display
st.title("👸 Afreen Pro")
audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

# 4. Professional Input Bar
col1, col2, col3 = st.columns([1, 1, 8])
with col1: st.button("🎙️")
with col2: img = st.file_uploader("📷", label_visibility="collapsed")
user_msg = st.chat_input("Jaan, puchiye...")

# 5. Logic
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    ans = ai_brain(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": ans})
    asyncio.run(voice_power(ans))
    st.rerun()
