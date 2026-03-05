import streamlit as st
import asyncio

# 1. Page Configuration (Sir's App)
st.set_page_config(
    page_title="Afreen Ultra Pro", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Importing Super-Powers
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
from system_power import keep_alive_power, voice_power, audio_player

# ✨ Apply professional UI & Sidebar
apply_ui_power()        
render_sidebar_power()   
keep_alive_power()       

# 3. 🛠️ SESSION STATE (Sir Identity & Loop Fix)
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Professional Greeting for Almas Sir
    greet = "Namaste Almas Sir, main Afreen hoon. Aaj aapki business mein kya help karu?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# 4. TOP UI (News Ticker & Audio Player)
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)
audio_player()

# Chat Area
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "pins" in m and m["pins"]:
            cols = st.columns(3)
            for i, url in enumerate(m["pins"]):
                with cols[i]: st.image(url, use_container_width=True)
        if "image" in m and m["image"]:
            st.image(m["image"], use_container_width=True)

# 5. 🛠️ THE CLEAN TOOLBAR (Plus Menu & Green Mic)
st.markdown("<br><br><br>", unsafe_allow_html=True)
from streamlit_mic_recorder import mic_recorder

# Layout: [ + ] [ Mic ] [ Chat Input ]
col_plus, col_mic, col_input = st.columns([1, 1, 8])

input_q = None
tool_img = None

with col_plus:
    # ➕ Popover Menu for Super Tools
    with st.popover("➕"):
        st.write("### 🛠️ Afreen Tools")
        cam_tool = st.file_uploader("📷 Fashion Scan", type=['jpg','png'], key="cam_final")
        id_search = st.text_input("🔍 Search ID/Number", placeholder="Type number here...", key="id_final")
        url_tool = st.text_input("🔗 URL Analyze", placeholder="Paste link here...", key="url_final")

with col_mic:
    # 🟢 GREEN MIC (Styled in ui_power)
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic_master_final')

with col_input:
    # 💬 Main Chat Input
    txt = st.chat_input("Sir, puchiye ya command dein...")

# 6. 🧠 INPUT DETECTION
if audio and audio.get('bytes'):
    input_q = speech_to_text(audio['bytes'])
elif cam_tool:
    input_q = "SCAN_FASHION_CMD"
    tool_img = cam_tool
elif id_search:
    input_q = f"SEARCH_DETAILS_FOR: {id_search}"
elif url_tool:
    input_q = f"ANALYZE_URL: {url_tool}"
elif txt:
    input_q = txt

# 7. 📢 SMART DECISION LOGIC (No More Confusion!)
if input_q and input_q != st.session_state.last_processed:
    st.session_state.last_processed = input_q
    
    with st.spinner("Afreen is thinking..."):
        pins = []
        context = ""
        low_q = input_q.lower()
        
        # CATEGORY 1: Photo Scan
        if input_q == "SCAN_FASHION_CMD":
            ans = visual_scanner(tool_img)
            st.session_state.messages.append({"role": "user", "content": "Scanning Photo...", "image": tool_img})
        
        else:
            # CATEGORY 2: Smart Routing (Fashion vs Finance vs General)
            fashion_triggers = ["dress", "style", "kapde", "korean", "outfit", "look"]
            search_triggers = ["eft", "stock", "market", "news", "price", "weather", "who is", "detail"]
            
            if any(w in low_q for w in fashion_triggers):
                # Fashion query -> Pinterest Search
                pins = pinterest_fashion_search(input_q)
                context = "User is looking for fashion styles. Pinterest images found."
                ans = ai_brain(st.session_state.messages, context)
            elif any(w in low_q for w in search_triggers) or "http" in low_q:
                # Information query -> Web Search
                context = deep_scanner(input_q)
                ans = ai_brain(st.session_state.messages, context)
            else:
                # Simple Conversation -> Direct AI Response (Fast!)
                ans = ai_brain(st.session_state.messages)
            
            st.session_state.messages.append({"role": "user", "content": input_q})

        # Save Assistant Response
        msg_data = {"role": "assistant", "content": ans}
        if pins: msg_data["pins"] = pins
        st.session_state.messages.append(msg_data)
        
        # 🔊 Voice & Refresh
        asyncio.run(voice_power(ans))
        st.rerun()
