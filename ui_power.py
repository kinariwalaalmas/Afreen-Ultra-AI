import streamlit as st

def apply_ui_power():
    """App ka professional look set karne ke liye"""
    st.markdown("""
    <style>
    .stApp { background-color: #fdf2f8; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stChatMessage { border-radius: 20px; box-shadow: 0 4px 15px rgba(219, 39, 119, 0.1); }
    [data-testid="stChatInput"] { position: fixed; bottom: 20px; z-index: 1000; background: white; border-radius: 25px; }
    .ticker-wrap { background: #fff1f2; padding: 10px; border-radius: 12px; border-left: 5px solid #db2777; color: #9d174d; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_power():
    """Sidebar (Side Menu) dikhane ke liye - Ye wala function missing tha!"""
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #db2777;'>👸 Afreen Ultra</h1>", unsafe_allow_html=True)
        st.divider()
        st.markdown("### 👤 Owner Details")
        st.info("Created & Owned by:\n**Almas Shaikh**")
        st.markdown("### 👕 Business Mode")
        st.success("Expert: **Surat Baggy & Korean Clothing**")
        st.divider()
        st.write("✨ *Afreen is always learning for Almas Jaan*")
