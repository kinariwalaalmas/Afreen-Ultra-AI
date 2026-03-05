import streamlit as st
import asyncio

st.set_page_config(page_title="Afreen Pro", layout="wide", initial_sidebar_state="collapsed")

# ✨ Name Matching Imports
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

if "messages" not in st.session_state:
    st.session_state.messages = []
    greet = "Namaste Almas Sir, main Afreen hoon. Aaj kya hukum hai?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

if "last_processed" not in st.session_state: st.session_state.last_processed = None

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

st.markdown("---")
from streamlit_mic_recorder import mic_recorder
c1, c2, c3 = st.columns([1, 1, 8])

input_q = None
with c1: audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_final')
with c2: 
    with st.popover("➕"):
        cam = st.file_uploader("📷 Scan", type=['jpg','png'], key="c")
        ids = st.text_input("🔍 Search", key="s")
with c3: txt = st.chat_input("Sir, puchiye...")

if audio and audio.get('bytes'): input_q = speech_to_text(audio['bytes'])
elif cam: input_q = "SCAN_FASHION"; tool_img = cam
elif ids: input_q = f"Search: {ids}"
elif txt: input_q = txt

if input_q and input_q != st.session_state.last_processed:
    st.session_state.last_processed = input_q
    with st.spinner("Processing..."):
        pins = []
        if input_q == "SCAN_FASHION": ans = visual_scanner(tool_img)
        else:
            if any(w in input_q.lower() for w in ["dress", "outfit", "style"]):
                pins = pinterest_fashion_search(input_q)
            context = deep_scanner(input_q)
            ans = ai_brain(st.session_state.messages, context)
        
        st.session_state.messages.append({"role": "user", "content": input_q})
        st.session_state.messages.append({"role": "assistant", "content": ans, "pins": pins})
        asyncio.run(voice_power(ans)); st.rerun()
