import streamlit as st

def apply_ui_power():
    """Isme saara Professional Look aur CSS merged hai"""
    st.markdown("""
    <style>
    /* 1. Full App Background & Font */
    .stApp { 
        background-color: #fdf2f8; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 2. Hide Streamlit Header & Footer for App Feel */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 3. Modern Chat Bubbles with Shadow */
    .stChatMessage { 
        border-radius: 20px; 
        box-shadow: 0 4px 15px rgba(219, 39, 119, 0.1); 
        border: 1px solid #fce7f3;
        margin-bottom: 12px;
    }
    
    /* 4. Sticky Bottom Input Bar Fix */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        z-index: 1000;
        background-color: white;
        border-radius: 25px;
        padding: 5px;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.05);
    }

    /* 5. News Ticker Styling */
    .ticker-wrap {
        background: #fff1f2;
        padding: 10px;
        border-radius: 12px;
        border-left: 5px solid #db2777;
        color: #9d174d;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_power():
    """Isme Sidebar wala saara business logic merged hai"""
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #db2777;'>👸 Afreen Ultra</h1>", unsafe_allow_html=True)
        st.divider()
        
        # Owner Info
        st.markdown("### 👤 Owner Details")
        st.info("Created & Owned by:\n**Almas Shaikh**")
        
        # Business Focus
        st.markdown("### 👕 Business Mode")
        st.success("Expert: **Surat Baggy & Korean Clothing**")
        
        st.divider()
        st.write("✨ *Afreen is always learning for Almas Jaan*")
