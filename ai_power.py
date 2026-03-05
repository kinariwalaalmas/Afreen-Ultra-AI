import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
from PIL import Image
import os

def get_ai_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def ai_brain(messages, context=""):
    """Afreen's Smart Personality"""
    try:
        _, groq_client = get_ai_clients()
        # ✨ IS PROMPT SE WO CONFUSE NAHI HOGI
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro. Tum Almas Shaikh (Jaan) ki Personal AI Assistant ho.
        
        RULES:
        1. Almas ko hamesha 'Jaan' kaho. Sweet Hinglish mein baat karo.
        2. Normal sawalon ka jawab turant aur akalmand assistant ki tarah do.
        3. Agar 'EFTs' pucha jaye, toh Stock Market investment (Exchange Traded Funds) samjho.
        4. Kabhi mat kehna 'I am a chatbot' ya 'I am confused'.
        
        CONTEXT: {context}
        """
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception: return "Jaan, mera server thoda busy hai, par main aapke saath hoon. Phir se puchiye na? ❤️"

# Baki functions (Pinterest, Search, etc.) same rahenge
def pinterest_fashion_search(query):
    try:
        with DDGS() as ddgs:
            res = [r['image'] for r in ddgs.images(f"{query} fashion pinterest", max_results=3)]
            return res
    except: return []

def deep_scanner(query):
    try:
        with DDGS() as ddgs:
            res = [r['body'] for r in ddgs.text(query, max_results=2)]
            return "\n".join(res)
    except: return ""

# Keep visual_scanner, get_news_ticker, speech_to_text as they are
