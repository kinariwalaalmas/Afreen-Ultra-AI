import streamlit as st
import asyncio

st.set_page_config(page_title="Afreen Pro", layout="wide", initial_sidebar_state="collapsed")

from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

# --- 🛠️ SESSION STATE & LOOP FIX ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    greet = "Namaste Almas Sir, main Afreen hoon. Aaj business mein kya madad karu?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

if "last_processed" not in st.session_state: st.session_state.last_processed = None

# UI Header
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)
audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "pins" in m:
            cols = st.columns(3)
            for i, url in enumerate(m["pins"]):
                with cols[i]: st.image(url, use_container_width=True)
        if "image" in m: st.image(m["image"])

# --- 🛠️ THE SUPER TOOLBAR ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
from streamlit_mic_recorder import mic_recorder

col_plus, col_mic, col_input = st.columns([1, 1, 8])
input_q = None
tool_img = None

with col_plus:
    with st.popover("➕"):
        st.write("### 🛠️ Super Tools")
        cam_tool = st.file_uploader("📷 Fashion Scan", type=['jpg','png'], key="cam_f")
        id_search = st.text_input("🔍 Search ID/Number", placeholder="Type number here...", key="id_s")
        url_tool = st.text_input("🔗 URL Analyze", placeholder="Paste link...", key="url_f")

with col_mic:
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_super_final')

with col_input:
    txt = st.chat_input("Sir, puchiye ya command dein...")

# Trigger Detection
if audio and audio.get('bytes'): input_q = speech_to_text(audio['bytes'])
elif cam_tool: input_q = "SCAN_FASHION"; tool_img = cam_tool
elif id_search: input_q = f"Search details for: {id_search}"
elif url_tool: input_q = f"Analyze URL: {url_tool}"
elif txt: input_q = txt

# --- 📢 SMART LOGIC EXECUTION ---
if input_q and input_q != st.session_state.last_processed:
    st.session_state.last_processed = input_q
    
    with st.spinner("Afreen is working..."):
        pins = []
        context = ""
        
        if input_q == "SCAN_FASHION":
            ans = visual_scanner(tool_img)
            st.session_state.messages.append({"role": "user", "content": "Scanning Photo...", "image": tool_img})
        else:
            # Smart Routing: Fashion vs Search vs General
            fashion_triggers = ["dress", "outfit", "style", "kapde", "korean"]
            search_triggers = ["eft", "stock", "market", "news", "price", "weather"]
            
            if any(w in input_q.lower() for w in fashion_triggers):
                pins = pinterest_fashion_search(input_q)
                context = "User is looking for fashion styles. Pinterest images found."
            elif any(w in input_q.lower() for w in search_triggers):
                context = deep_scanner(input_q)
            
            ans = ai_brain(st.session_state.messages, context)
            st.session_state.messages.append({"role": "user", "content": input_q})

        st.session_state.messages.append({"role": "assistant", "content": ans, "pins": pins})
        asyncio.run(voice_power(ans))
        st.rerun()
