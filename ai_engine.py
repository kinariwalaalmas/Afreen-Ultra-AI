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

def get_ai_response(messages, search_info=""):
    """Teeno Brains ka automatic combo!"""
    gemini_client, groq_client = get_clients()
    system_prompt = f"You are Afreen, a sweet Hinglish girl. Use MASCULINE grammar. User is 'Jaan'. Context: {search_info}"
    
    user_query = messages[-1]["content"].lower()
    
    try:
        # 1. Complex/Logical sawalon ke liye DeepSeek-R1
        if any(word in user_query for word in ["socho", "plan", "business", "detail", "why"]):
            res = groq_client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[{"role": "system", "content": system_prompt}] + messages
            )
            return res.choices[0].message.content
        
        # 2. Fast chat ke liye Llama 3.3
        elif len(user_query) > 50:
            res = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + messages
            )
            return res.choices[0].message.content
            
        # 3. Baaki sab ke liye Gemini 1.5 Flash
        else:
            chat = gemini_client.start_chat(history=[])
            response = chat.send_message(f"{system_prompt}\n\nUser: {user_query}")
            return response.text
    except:
        return "Jaan, dimaag ki thodi wires ulajh gayi hain, par main phir bhi aapke saath hoon!"

# ... Baki voice/search functions wese hi rahenge ...
