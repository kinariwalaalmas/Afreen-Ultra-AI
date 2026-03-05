import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #fdf2f8; padding-bottom: 100px; }
    
    /* Hide Default Streamlit Elements for a clean App feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fixed Bottom Container for Professional Toolbar */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 10px 15px;
        border-top: 1px solid #fecdd3;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Message Bubbles */
    .stChatMessage { 
        border-radius: 20px; 
        margin-bottom: 10px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Styling the icons */
    .icon-btn {
        font-size: 24px;
        cursor: pointer;
        padding: 5px;
    }

    /* Ensuring mobile keyboard pushes the content correctly */
    @media screen and (max-width: 600px) {
        .stChatInput {
            bottom: 10px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
