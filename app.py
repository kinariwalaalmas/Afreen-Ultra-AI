import streamlit as st
import asyncio

# 1. Page Configuration
st.set_page_config(
    page_title="Afreen Ultra Pro", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Importing Your Super-Powers
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

# ✨ Applying UI Styles & Sidebar
apply_ui_power()        
render_sidebar_power()   
keep_alive_power()       

# 3. 🛠️ SESSION STATE & LOOP PREVENTION
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Professional Greeting for Almas Sir
    greet = "Namaste Almas Sir, main Afreen hoon. Aaj Surat market ya aapke business mein kya help karu?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# 4. UI DISPLAY (News Ticker & Audio)
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)
audio_player()

# Chat History Area
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "pins" in m and m["pins"]:
            cols = st.columns(3)
            for i, url in enumerate(m["pins"]):
                with cols[i]: st.image(url, use_container_width=True)
        if "image" in m and m["image"]:
            st.image(m["image"], use_container_width=True)

# 5. 🛠️ THE PROFESSIONAL TOOLBAR (Plus Menu & Green Mic)
st.markdown("<br><br><br>", unsafe_allow_html=True)
from streamlit_mic_recorder import mic_recorder

# Layout: [ + ] [ Mic ] [ Chat Input ]
col_plus, col_mic, col_input = st.columns([1, 1, 8])

input_q = None
tool_img = None

with col_plus:
    # ➕ Super Tools Menu (Clean Popover)
    with st.popover("➕"):
        st.write("### 🛠️ Afreen Super Tools")
        cam_tool = st.file_uploader("📷 Fashion Scan", type=['jpg','png'], key="cam_f_final")
        id_search_val = st.text_input("🔍 Search ID/Number", placeholder="Type number here...", key="id_s_final")
        url_tool_val = st.text_input("🔗 URL Analyze", placeholder="Paste link here...", key="url_f_final")

with col_mic:
    # 🟢 GREEN MIC (Always Visible)
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_super_master')

with col_input:
    # 💬 Modern Chat Input
    txt = st.chat_input("Sir, puchiye ya command dein...")

# 6. 🧠 INPUT DETECTION & LOGIC
if audio and audio.get('bytes'):
    input_q = speech_to_text(audio['bytes'])
elif cam_tool:
    input_q = "SCAN_FASHION_CMD"
    tool_img = cam_tool
elif id_search_val:
    input_q = f"SEARCH_ID_DATA: {id_search_val}"
elif url_tool_val:
    input_q = f"URL_ANALYZE: {url_tool_val}"
elif txt:
    input_q = txt

# 7. EXECUTION (Loop Protection)
if input_q and input_q != st.session_state.last_processed:
    st.session_state.last_processed = input_q
    
    with st.spinner("Afreen is working..."):
        pins = []
        context = ""
        
        # CATEGORY 1: Photo/Fashion Scan
        if input_q == "SCAN_FASHION_CMD":
            ans = visual_scanner(tool_img)
            st.session_state.messages.append({"role": "user", "content": "Scanning Fashion Photo...", "image": tool_img})
        
        # CATEGORY 2: Smart Search & URL Logic
        elif "SEARCH_ID_DATA" in input_q or "URL_ANALYZE" in input_q:
            context = deep_scanner(input_q)
            ans = ai_brain(st.session_state.messages, context)
            st.session_state.messages.append({"role": "user", "content": input_q})
            
        else:
            # CATEGORY 3: General Talk, Fashion Triggers, or Stocks/EFTs
            fashion_words = ["dress", "outfit", "style", "kapde", "korean", "baggy"]
            search_words = ["eft", "stock", "news", "price", "market", "weather"]
            
            if any(w in input_q.lower() for w in fashion_words):
                pins = pinterest_fashion_search(input_q)
                context = "User is looking for fashion styles. Pinterest images found."
            elif any(w in input_q.lower() for w in search_words):
                context = deep_scanner(input_q)
            
            ans = ai_brain(st.session_state.messages, context)
            st.session_state.messages.append({"role": "user", "content": input_q})

        # Save & Finalize
        msg_data = {"role": "assistant", "content": ans}
        if pins: msg_data["pins"] = pins
        st.session_state.messages.append(msg_data)
        
        # 🔊 Speak & Refresh
        asyncio.run(voice_power(ans))
        st.rerun()
