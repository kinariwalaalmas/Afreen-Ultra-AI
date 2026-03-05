import streamlit as st
import asyncio

# 1. Page Config
st.set_page_config(page_title="Afreen Pro", layout="wide")

from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

# --- 🛠️ ADVANCED LOOP PREVENTER ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Sirf pehli baar swagat
    greet = "Hey Almas Jaan, main Afreen hoon. Aaj kya help karu?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

# Pichli query ko yaad rakhne ke liye taaki repeat na ho
if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

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

input_query = None
with c1: audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic')
with c2: img = st.file_uploader("📷", type=['jpg','png'], label_visibility="collapsed", key="camera")
with c3: txt = st.chat_input("Jaan, boliye...")

# Input detection
if audio and audio.get('bytes'):
    input_query = speech_to_text(audio['bytes'])
elif img: 
    input_query = "SCAN_IMAGE_COMMAND"
elif txt: 
    input_query = txt

# --- 📢 LOGIC HANDLER (Loop Fix) ---
# Sirf tabhi chalo jab nayi query aayi ho
if input_query and input_query != st.session_state.last_processed:
    st.session_state.last_processed = input_query # Ise lock kar do!
    
    st.session_state.messages.append({"role": "user", "content": "Command received..." if input_query == "SCAN_IMAGE_COMMAND" else input_query})
    
    with st.spinner("Afreen is processing..."):
        pins = []
        if input_query == "SCAN_IMAGE_COMMAND":
            ans = visual_scanner(img)
        else:
            # Pinterest & Search logic
            fashion_words = ["dress", "outfit", "style", "kapde", "korean", "baggy"]
            if any(w in input_query.lower() for w in fashion_words):
                pins = pinterest_fashion_search(input_query)
            
            context = deep_scanner(input_query)
            ans = ai_brain(st.session_state.messages, context)
        
        # Save & Respond
        msg_data = {"role": "assistant", "content": ans}
        if pins: msg_data["pins"] = pins
        st.session_state.messages.append(msg_data)
        
        # Speak & Finish
        asyncio.run(voice_power(ans))
        st.rerun() # Refresh to update UI and Stop Loop
