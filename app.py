import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio, web_search, get_ai_response
from ui_components import render_plus_menu, render_sidebar, render_quick_actions
from vision_logic import analyze_image
from finance_expert import get_stock_analysis
from phone_control import get_phone_action

# 1. Configuration & Theme
st.set_page_config(page_title="Afreen Ultra Pro", page_icon="💎", layout="wide")
apply_styles()
selected_brain = render_sidebar() # Sidebar se model choose karna

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Clients Initialization
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("⚠️ Jaan, API Keys check kijiye Secrets mein!")
    st.stop()

st.title("👸 Afreen")

# 3. Tools Menu
audio_data, uploaded_photo, stock_ticker = render_plus_menu()

# 4. Quick Actions
if not st.session_state.messages:
    render_quick_actions()

# 5. Input Handling
user_msg = st.chat_input("Jaan, boliye...")
if audio_data:
    user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# 6. LOGIC & ACTIONS
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)
    
    action_url, action_msg = get_phone_action(user_msg) # App Opener
    
    if action_url:
        st.info(action_msg)
        st.link_button("Execute Now 🚀", action_url, use_container_width=True)
    else:
        with st.spinner(f"Afreen ({selected_brain}) is thinking..."):
            search_info = ""
            if any(x in user_msg.lower() for x in ["news", "market", "bhav", "trend"]):
                search_info = f"\nSearch Info: {web_search(user_msg)}"
            
            # Multi-Brain Routing
            ans = get_ai_response(selected_brain, st.session_state.messages, search_info)
            
            st.session_state.messages.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"): st.write(ans)
            asyncio.run(generate_voice(ans))
            play_audio()

# 7. Media Processing
if uploaded_photo:
    st.image(uploaded_photo, width=150)
    if st.button("Analyze Photo 🔍"):
        res = analyze_image(GEMINI_KEY, uploaded_photo)
        st.write(res)
        asyncio.run(generate_voice(res))
        play_audio()

if stock_ticker:
    if st.button(f"Analyze {stock_ticker} 📈"):
        res = get_stock_analysis(gemini_model, stock_ticker)
        st.write(res)
        asyncio.run(generate_voice(res))
        play_audio()

for message in st.session_state.messages[:-1]:
    with st.chat_message(message["role"]): st.write(message["content"])
