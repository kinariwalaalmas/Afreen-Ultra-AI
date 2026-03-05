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

# ✨ Applying Professional Look & Sidebar
apply_ui_power()        
render_sidebar_power()   
keep_alive_power()       

# 3. 🛠️ SESSION STATE & LOOP PREVENTION
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Auto-Greeting
    greet = "Hey Almas Jaan, main Afreen hoon. Aaj Surat ke business mein kya dhamaka karna hai?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# 4. UI DISPLAY (News Ticker & Audio Player)
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)
audio_player()

# Chat History Display
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
        cam_tool = st.file_uploader("📷 Fashion Scan", type=['jpg','png'], key="cam_f")
        id_search = st.text_input("🔍 Search ID/Number", placeholder="Type number here...", key="id_s")
        url_tool = st.text_input("🔗 URL Analyze", placeholder="Paste link here...", key="url_f")

with col_mic:
    # 🟢 GREEN MIC (Styled in ui_power)
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_super_final')

with col_input:
    # 💬 Modern Chat Input
    txt = st.chat_input("Jaan, puchiye ya command dein...")

# 6. 🧠 SMART DECISION LOGIC (Identifying Command Type)
if audio and audio.get('bytes'):
    input_q = speech_to_text(audio['bytes'])
elif cam_tool:
    input_q = "SCAN_FASHION_COMMAND"
    tool_img = cam_tool
elif id_search:
    input_q = f"SEARCH_ID_NUMBER: {id_search}"
elif url_tool:
    input_q = f"ANALYZE_URL: {url_tool}"
elif txt:
    input_q = txt

# 7. EXECUTION (Running only if new command)
if input_q and input_q != st.session_state.last_processed:
    st.session_state.last_processed = input_q
    
    with st.spinner("Afreen is working..."):
        pins = []
        context = ""
        
        # CATEGORY 1: Fashion Scan
        if input_q == "SCAN_FASHION_COMMAND":
            ans = visual_scanner(tool_img)
            st.session_state.messages.append({"role": "user", "content": "Analyzing Fashion...", "image": tool_img})
        
        # CATEGORY 2: ID Search or URL Analyze
        elif "SEARCH_ID_NUMBER" in input_q or "ANALYZE_URL" in input_q:
            context = deep_scanner(input_q)
            ans = ai_brain(st.session_state.messages, context)
            st.session_state.messages.append({"role": "user", "content": input_q})
            
        else:
            # CATEGORY 3: General or Pinterest Fashion
            fashion_triggers = ["dress", "outfit", "style", "kapde", "korean", "baggy"]
            search_triggers = ["eft", "stock", "news", "price", "market", "weather"]
            
            if any(w in input_q.lower() for w in fashion_triggers):
                pins = pinterest_fashion_search(input_q)
                context = "User is looking for fashion styles. Pinterest images found."
            elif any(w in input_q.lower() for w in search_triggers):
                context = deep_scanner(input_q)
            
            ans = ai_brain(st.session_state.messages, context)
            st.session_state.messages.append({"role": "user", "content": input_q})

        # Save Assistant Response
        msg_data = {"role": "assistant", "content": ans}
        if pins: msg_data["pins"] = pins
        st.session_state.messages.append(msg_data)
        
        # 📢 Voice & UI Refresh
        asyncio.run(voice_power(ans))
        st.rerun()
