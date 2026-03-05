import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    """Afreen ka sidebar setup"""
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>👸 Afreen Pro</h2>", unsafe_allow_html=True)
        st.write("---")
        st.success("⚡ **Dual-Turbo Brain Active**")
        st.write("Google + Groq (Powered)")
        st.divider()
        st.write("👕 **Surat Market Expert**")
        st.write("Specialist: Baggy & Korean Styles")

def render_plus_menu():
    """Plus button ke andar ke tools"""
    with st.popover("＋", help="Tools"):
        audio = mic_recorder(start_prompt="Record 🎤", stop_prompt="Stop 🛑", key='mic')
        st.divider()
        photo = st.file_uploader("Upload Fabric Photo", type=["jpg", "png"])
        ticker = st.text_input("Stock Analysis (Symbol)")
    return audio, photo, ticker

def render_quick_actions():
    """Home screen ke shortcut cards"""
    st.write("### Jaan, aaj kya plan hai?")
    col1, col2 = st.columns(2)
    with col1: 
        st.markdown('<div style="padding:20px; border-radius:10px; background-color:#f0f2f6; text-align:center;">👕 Surat Trends</div>', unsafe_allow_html=True)
    with col2: 
        st.markdown('<div style="padding:20px; border-radius:10px; background-color:#f0f2f6; text-align:center;">📈 Market News</div>', unsafe_allow_html=True)
