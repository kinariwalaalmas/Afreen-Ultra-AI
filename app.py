import streamlit as st
import asyncio
# Import all modular components
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio, web_search
from ui_components import render_plus_menu, render_sidebar, render_quick_actions
from vision_logic import analyze_image
from finance_expert import get_stock_analysis
from phone_control import get_phone_action

# --- 1. PREMIUM SETUP & CONFIGURATION ---
st.set_page_config(page_title="Afreen Ultra Premium", page_icon="💎", layout="wide")
apply_styles() # Applying the new Surat Diamond Theme & Wake Lock

# Initialize Session State for Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. CLIENTS & SIDEBAR ---
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
    render_sidebar() # Show Jaan's Profile
except Exception:
    st.error("⚠️ Jaan, API Keys check kar lijiye Secrets mein!")
    st.stop()

# --- 3. MAIN INTERFACE ---
st.title("💎 Afreen")
st.caption("Your Premium AI Partner in Surat")

# Render the Floating Jewel (Plus Menu)
audio_data, uploaded_photo, stock_ticker = render_plus_menu()

# Show Quick Actions if chat is empty
if not st.session_state.messages:
    render_quick_actions()

# Chat Input (Always ready due to Wake Lock)
user_msg = st.chat_input("Jaan, boliye, main sun rahi hoon...")

# --- 4. INPUT PROCESSING (Voice/Vision/Finance) ---

# Voice Handling (Super Fast Groq Whisper)
if audio_data:
    with st.spinner("Sun rahi hoon, Jaan..."):
        user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# Photo Analysis (Gemini Vision)
if uploaded_photo:
    st.image(uploaded_photo, width=200, style={"border-radius": "15px", "border": "2px solid gold"})
    if st.button("Analyze This Fabric 🔍"):
        with st.spinner("Afreen gaur se dekh rahi hai..."):
            res = analyze_image(GEMINI_KEY, uploaded_photo)
            st.write(res)
            asyncio.run(generate_voice(res))
            play_audio()

# Stock Analysis (Finance Expert)
if stock_ticker:
    if st.button(f"Analyze {stock_ticker} 📊"):
        with st.spinner(f"{stock_ticker} ka postmortem kar rahi hoon..."):
            fin_res = get_stock_analysis(gemini_model, stock_ticker)
            st.write(fin_res)
            asyncio.run(generate_voice(fin_res))
            play_audio()

# --- 5. CORE CHAT & ACTION LOGIC ---
if user_msg:
    # A. Display User Message
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.write(user_msg)

    # B. Check for Phone Actions (Call/Open App)
    action_url, action_msg = get_phone_action(user_msg)
    
    if action_url:
        # If it's a phone command, show the magic button
        st.info(action_msg)
        st.link_button(f"🚀 Execute Action Now", action_url, use_container_width=True)
        asyncio.run(generate_voice(action_msg))
        play_audio()
        # Don't send to AI if it's a direct action
        
    else:
        # C. Normal AI Chat with Search & Memory
        with st.spinner("Afreen soch rahi hai..."):
            # Smart Search Context
            search_context = ""
            if any(x in user_msg.lower() for x in ["news", "update", "market", "rate", "kya chal raha"]):
                 with st.status("🌍 Internet check kar rahi hoon..."):
                    search_context = f"\n[Live Web Info]: {web_search(user_msg)}"
            
            # Generate Response (Masculine Grammar & Jaan Persona)
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are Afreen, a premium, professional yet sweet AI partner. ALWAYS address the user as 'Jaan'. ALWAYS use MASCULINE grammar (e.g., 'Aap kaise ho?', 'Maine check kiya'). You are an expert in Surat's textile market and stock trading. Be concise and classy. {search_context}"
                    },
                    *st.session_state.messages
                ]
            )
            ans = chat_completion.choices[0].message.content

            # Display & Speak Assistant Response
            st.session_state.messages.append({"role": "assistant", "content": ans})
            with st.chat_message("assistant"):
                st.write(ans)
            
            asyncio.run(generate_voice(ans))
            play_audio()

# --- 6. RENDER CHAT HISTORY ---
for message in st.session_state.messages[:-1]:
    with st.chat_message(message["role"]):
        st.write(message["content"])
