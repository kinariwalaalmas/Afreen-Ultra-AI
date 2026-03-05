import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>👸 Afreen Ultra</h2>", unsafe_allow_html=True)
        st.write("---")
        st.success("🚀 **Triple-Power Brain Active**")
        st.write("Google + Groq + DeepSeek")
        st.divider()
        st.info("Expertise: Surat Baggy Clothing Market")
        st.write("📍 Location: Ring Road, Surat")

# ... render_plus_menu and quick_actions same rahenge ...
