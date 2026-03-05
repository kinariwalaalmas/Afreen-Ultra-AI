import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>👸 Afreen Pro</h2>", unsafe_allow_html=True)
        st.info("👕 **Surat Market Expert**")
        st.write("Owner: **Almas Shaikh**")
        st.divider()
        st.success("✅ Business Logic Active")
