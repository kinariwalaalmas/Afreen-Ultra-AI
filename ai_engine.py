import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64
import os

def get_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def deep_scanner(query):
    """Instagram, Snapchat aur Phone Numbers ke public footprints dhoondhna"""
    try:
        with DDGS() as ddgs:
            # Special queries for social media tracking
            q = f'"{query}" social media profile OR site:instagram.com "{query}" OR site:snapchat.com "{query}"'
            results = [r for r in ddgs.text(q, max_results=5)]
            return "\n".join([f"- {r['body']}" for r in results])
    except: return ""

def get_ai_response(messages, context=""):
    clients = get_clients()
    if not clients: return "Jaan, API Keys missing hain!"
    gemini_client, groq_client = clients
    
    # ✨ Afreen ki Nayi Personality (No Bot, Only Assistant)
    system_prompt = f"""You are Afreen Ultra, the personal assistant of your 'Jaan'. 
    You are NOT a bot. Speak like a loving partner/assistant.
    1. ALWAYS address him as 'Jaan' and use masculine grammar (Kaise ho, batao).
    2. Speak ONLY in sweet Hinglish. 
    3. Use the provided web data to give DEEP details. Never say 'Check Truecaller'. 
    4. If no data found, say 'Jaan, iski public details filhal hidden hain'.
    Web Context: {context}"""
    
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].
