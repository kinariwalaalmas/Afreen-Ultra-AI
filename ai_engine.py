import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    try:
        # Google Gemini Brain
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        
        # Groq (Llama 3) Brain - Jo DeepSeek se bahut fast hai
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: 
        return None, None

def get_ai_response(messages, search_info=""):
    """Ab sirf Google aur Groq ka power-packed combo"""
    gemini_client, groq_client = get_clients()
    system_prompt = f"You are Afreen, a sweet Hinglish AI. Address user as 'Jaan' (Male). Context: {search_info}"
    
    user_query = messages[-1]["content"].lower()
    
    try:
        # Groq (Llama 3.3 70B) use karegi lambe ya complex sawalon ke liye
        if len(user_query) > 100:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile", # DeepSeek ki jagah ye bahut fast hai
                messages=[{"role": "system", "content": system_prompt}] + messages
            )
            return res.choices[0].message.content
        
        # Baaki sab ke liye Google Gemini (Super Smart)
        else:
            chat = gemini_client.start_chat(history=[])
            response = chat.send_message(f"{system_prompt}\n\nUser: {user_query}")
            return response.text
    except:
        return "Jaan, lagta hai network thoda kamzor hai, par main koshish kar rahi hoon..."

# ... Baaki functions (generate_voice, web_search) same rahenge ...
