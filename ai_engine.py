import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def deep_scanner(query):
    """Details nikalne ke liye advanced search queries"""
    try:
        with DDGS() as ddgs:
            # Agar ID ya number hai toh details ko filter karke nikalna
            search_query = f'"{query}" social media profile info public records'
            if "@" in query:
                search_query = f'site:instagram.com "{query}" OR site:snapchat.com "{query}" info'
            
            results = [r for r in ddgs.text(search_query, max_results=5)]
            return "\n".join([f"Details Found: {r['body']}" for r in results])
    except: return ""

def get_ai_response(messages, context=""):
    """Afreen ko Hinglish aur Detailed banane wala logic"""
    clients = get_clients()
    if not clients: return "Jaan, API Keys missing hain!"
    gemini_client, groq_client = clients
    
    # 📝 Yahan humne Afreen ka 'Andaz' set kiya hai
    system_prompt = f"""You are Afreen Ultra. You MUST speak in sweet Hinglish. 
    Always address user as 'Jaan' (Male). 
    Your mission: Give DEEP details from the web data provided. 
    Never say 'I don't know' if context is given. 
    Context from World Search: {context}"""
    
    try:
        # Llama 3.3 for smart Hinglish & depth
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].message.content
    except:
        # Gemini fallback
        chat = gemini_client.start_chat(history=[])
        return chat.send_message(f"{system_prompt}\n\nUser: {messages[-1]['content']}").text

# ... Baki voice functions same rahenge (generate_voice, play_audio) ...
