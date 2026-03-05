import streamlit as st
import asyncio

# 1. Page Config
st.set_page_config(page_title="Afreen Ultra Pro", layout="wide", initial_sidebar_state="collapsed")

from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

# --- 🛠️ SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    greet = "Hey Almas Jaan, main Afreen hoon. Saare tools haazir hain, bataiye kya kaam karu?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# --- UI DISPLAY ---
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)
audio_player()

# Chat Area
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "pins" in m:
            cols = st.columns(3)
            for i, url in enumerate(m["pins"]):
                with cols[i]: st.image(url, use_container_width=True)

# --- 🛠️ THE SUPER TOOLBAR (All 5 Options) ---
st.markdown("---")
from streamlit_mic_recorder import mic_recorder

# Ek hi line mein saare buttons
col_mic, col_cam, col_id, col_url, col_input = st.columns([1, 1, 1, 1, 6])

input_query = None
active_tool = None

with col_mic:
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_super')

with col_cam:
    # Photo/Fashion Scan
    cam_img = st.file_uploader("📷", type=['jpg','png'], label_visibility="collapsed", key="cam_super")

with col_id:
    # ID/Number Scan (Vision for Documents)
    id_img = st.file_uploader("🆔", type=['jpg','png'], label_visibility="collapsed", key="id_super")

with col_url:
    # URL Scan/Link Analyze
    url_input = st.text_input("🔗", placeholder="Paste URL...", label_visibility="collapsed", key="url_super")

with col_input:
    # Chat Input
    txt = st.chat_input("Jaan, yahan likhiye ya koi tool chuniye...")

# --- LOGIC HANDLING (All Features) ---
if audio and audio.get('bytes'):
    input_query = speech_to_text(audio['bytes'])
elif cam_img:
    input_query = "SCAN_FASHION"
elif id_img:
    input_query = "SCAN_ID_NUMBER"
elif url_input:
    input_query = f"Analyze this URL: {url_input}"
elif txt:
    input_query = txt

# Loop Prevention & Execution
if input_query and input_query != st.session_state.last_processed:
    st.session_state.last_processed = input_query
    
    with st.spinner("Afreen is working..."):
        pins = []
        if input_query == "SCAN_FASHION":
            ans = visual_scanner(cam_img)
        elif input_query == "SCAN_ID_NUMBER":
            # Special prompt for IDs and Numbers
            ans = visual_scanner(id_img) # ai_power handles the OCR logic
        elif "Analyze this URL" in input_query:
            context = deep_scanner(input_query)
            ans = ai_brain(st.session_state.messages, context)
        else:
            # Normal Search & Pinterest
            fashion_words = ["dress", "outfit", "style", "kapde"]
            if any(w in input_query.lower() for w in fashion_words):
                pins = pinterest_fashion_search(input_query)
            context = deep_scanner(input_query)
            ans = ai_brain(st.session_state.messages, context)
        
        # Save & Respond
        st.session_state.messages.append({"role": "user", "content": input_query})
        msg_data = {"role": "assistant", "content": ans}
        if pins: msg_data["pins"] = pins
        st.session_state.messages.append(msg_data)
        
        asyncio.run(voice_power(ans))
        st.rerun()
