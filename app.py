import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio, web_search
from ui_components import render_plus_menu, render_sidebar, render_quick_actions
from vision_logic import analyze_image
from finance_expert import get_stock_analysis
from phone_control import get_phone_action

# 1. Page Configuration & Professional Theme
st.set_page_config(page_title="Afreen Ultra Pro", page_icon="👸", layout="wide")
apply_styles() # Styles.py se Glassmorphism UI aayega
render_sidebar() # Sidebar mein Jaan ka profile dikhega

# 2. Chat History (Memory) Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. AI Clients Initialization
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("⚠️ Jaan, please check your API Keys in Streamlit Secrets!")
    st.stop()

st.title("👸 Afreen")

# 4. Gemini-Style Tools Menu (Floating Plus Button)
audio_data, uploaded_photo, stock_ticker = render_plus_menu()

# 5. Quick Action Cards (Jab chat khali ho)
if not st.session_state.messages:
    render_quick_actions()

# 6. Chat Input & Voice Processing
user_msg = st.chat_input("Jaan, mujhse kuch bhi puchiye...")

# Voice to Text Handling
if audio_data:
    with st.spinner("Processing voice..."):
        user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# 7. LOGIC PROCESSING (Actions, Vision, Finance)

# A. Phone Control (App Opener/Alarm/Call)
action_url, action_msg = None, None
if user_msg:
    action_url, action_msg = get_phone_action(user_msg)

# B. Photo Analysis (GSM/Fabric)
if uploaded_photo:
    st.image(uploaded_photo, width=200, caption="Selected Fabric")
    if st.button("Analyze Fabric 🔍"):
        with st.spinner("Afreen dekh rahi hai..."):
            res = analyze_image(GEMINI_KEY, uploaded_photo)
            st.write(res)
            asyncio.run(generate_voice(res)) #
            play_audio()

# C. Stock/ETF Analysis
if stock_ticker:
    if st.button(f"Analyze {stock_ticker} 📈"):
        with st.spinner(f"Checking {stock_ticker} reports..."):
            fin_res = get_stock_analysis(gemini_model, stock_ticker)
            st.write(fin_res)
            asyncio.run(generate_voice(fin_res))
            play_audio()

# 8. MAIN CHAT & RESPONSE LOGIC
if user_msg:
    # Display User Message
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.write(user_msg)

    with st.spinner("Afreen is thinking..."):
        if action_url:
            # Handle App Opening
            st.info(action_msg)
            st.link_button(f"Open Now 🚀", action_url, use_container_width=True)
            ans = action_msg
        else:
            # Handle Web Search if needed
            search_context = ""
            if any(x in user_msg.lower() for x in ["news", "market", "bhav", "trend"]):
                search_context = f"\nRecent Search Info: {web_search(user_msg)}"
            
            # AI Response with Memory & Search
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are Afreen, a sweet Hinglish girl. Address the user as 'Jaan'. ALWAYS use MASCULINE grammar (Kaise ho). You are an expert in Surat baggy clothes and stocks. {search_context}"
                    },
                    *st.session_state.messages
                ]
            )
            ans = chat_completion.choices[0].message.content

        # Display Assistant Message
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"):
            st.write(ans)
        
        # Voice Output
        asyncio.run(generate_voice(ans))
        play_audio()

# 9. Display Chat History
for message in st.session_state.messages[:-1]: # Latest message already shown above
    with st.chat_message(message["role"]):
        st.write(message["content"])
