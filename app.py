import streamlit as st
import asyncio

# 1. Config & Share Fix
st.set_page_config(page_title="Afreen Pro", layout="wide", menu_items={'About': "Created by Almas Shaikh"})

from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

# --- 🛠️ SESSION LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Auto Greeting
    greet = "Hey Almas Jaan, main Afreen hoon. Aaj business kaisa hai?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

# --- 🎙️ AUTO-READY MIC ---
st.components.v1.html("<script>navigator.mediaDevices.getUserMedia({audio:true});</script>", height=0)

# --- UI ---
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)
audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "pins" in m:
            cols = st.columns(3)
            for i, url in enumerate(m["pins"]):
                with cols[i]: st.image(url, use_container_width=True)

# --- TOOLBAR ---
st.markdown("---")
from streamlit_mic_recorder import mic_recorder
c1, c2, c3 = st.columns([1, 1, 8])

final_q = None
with c1: audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic')
with c2: img = st.file_uploader("📷", type=['jpg','png'], label_visibility="collapsed")
with c3: txt = st.chat_input("Jaan, boliye...")

if audio and audio.get('bytes'):
    final_q = speech_to_text(audio['bytes'])
elif img: final_q = "Analyze image"
elif txt: final_q = txt

# --- 📢 VOICE RESPONSE LOGIC ---
if final_q:
    st.session_state.messages.append({"role": "user", "content": final_q})
    with st.chat_message("user"): st.write(final_q)

    with st.spinner("Afreen is working..."):
        pins = []
        if img:
            ans = visual_scanner(img)
        else:
            # Pinterest Check
            fashion_words = ["dress", "outfit", "style", "kapde", "korean", "baggy"]
            if any(w in final_q.lower() for w in fashion_words):
                pins = pinterest_fashion_search(final_q)
            
            context = deep_scanner(final_q)
            ans = ai_brain(st.session_state.messages, context)
        
        # Save & Speak
        msg_data = {"role": "assistant", "content": ans}
        if pins: msg_data["pins"] = pins
        
        st.session_state.messages.append(msg_data)
        
        # 🔊 Har command par bolne ke liye
        asyncio.run(voice_power(ans))
        st.rerun()
