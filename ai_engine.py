import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS # Ye ekdum free hai Jaan!
import edge_tts
import asyncio
import base64

def get_clients():
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    return groq_client

# --- Free Unlimited Search Logic ---
def web_search(query):
    try:
        with DDGS() as ddgs:
            # Ye top 3 results nikal lega
            results = [r for r in ddgs.text(query, max_results=3)]
            if results:
                # Pehle result ka snippet return karega
                return results[0]['body']
        return "Search results nahi mile, Jaan."
    except Exception as e:
        return f"Internet connection mein issue hai: {str(e)}"

# Voice aur Baki functions pehle jaise hi rahenge...
