import streamlit as st
import asyncio

st.set_page_config(page_title="Afreen Ultra", layout="wide", initial_sidebar_state="collapsed")

from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

# --- SESSION LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    greet = "Hey Almas Jaan, main Afreen hoon. Ab aap ID/Number seedha search kar sakte hain! ✨"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

if "last_processed" not in st.session_state: st.session_state.last_processed = None

# UI Display
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)
audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "pins" in m:
            cols = st.columns(3)
            for i, url in enumerate(m["pins"]):
                with cols[i]: st.image(url, use_container_width=True)

# --- 🛠️ THE NEW CLEAN TOOLBAR ---
st.markdown("---")
from streamlit_mic_recorder import mic_recorder

# Layout: [ + ] [ Mic ] [ Chat Input ]
col_plus, col_mic, col_input = st.columns([1, 1, 8])

input_q = None
tool_img = None

with col_plus:
    # ➕ Super Tools Menu
    with st.popover("➕"):
        st.write("### 🛠️ Afreen Tools")
        cam_tool = st.file_uploader("📷 Fashion Scan", type=['jpg','png'], key="cam_f")
        # ✨ ID SCAN SEARCH BOX (Replacing Browse File)
        id_search = st.text_input("🔍 Search ID/Number", placeholder="Type number here...", key="id_s")
        url_tool = st.text_input("🔗 URL Analyze", placeholder="Paste link...", key="url_f")

with col_mic:
    # 🟢 GREEN MIC (Always Visible)
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_gr_final')

with col_input:
    txt = st.chat_input("Jaan, puchiye ya command dein...")

# --- LOGIC HANDLING ---
if audio and audio.get('bytes'): 
    input_q = speech_to_text(audio['bytes'])
elif cam_tool: 
    input_q = "SCAN_FASHION"; tool_img = cam_tool
elif id_search: 
    # Jab aap number type karke Enter dabayenge
    input_q = f"Search ID or Number details for: {id_search}"
elif url_tool: 
    input_q = f"Analyze URL: {url_tool}"
elif txt: 
    input_q = txt

if input_q and input_q != st.session_state.last_processed:
    st.session_state.last_processed = input_q
    with st.spinner("Afreen is working..."):
        pins = []
        if input_q == "SCAN_FASHION": 
            ans = visual_scanner(tool_img)
        else:
            if any(w in input_q.lower() for w in ["dress", "style", "kapde"]):
                pins = pinterest_fashion_search(input_q)
            context = deep_scanner(input_q)
            ans = ai_brain(st.session_state.messages, context)
        
        st.session_state.messages.append({"role": "user", "content": input_q})
        msg_data = {"role": "assistant", "content": ans}
        if pins: msg_data["pins"] = pins
        st.session_state.messages.append(msg_data)
        asyncio.run(voice_power(ans)); st.rerun()
