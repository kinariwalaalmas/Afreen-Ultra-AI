import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>👸 Afreen Pro</h2>", unsafe_allow_html=True)
        st.write("---")
        st.success("⚡ **Dual-Turbo Brain Active**")
        st.write("Powered by Google & Groq")
        st.divider()
        st.write("👕 **Surat Market Expert**")
        st.write("Specialist: Baggy & Korean Styles")

# ... render_plus_menu and quick_actions same rahenge ...
