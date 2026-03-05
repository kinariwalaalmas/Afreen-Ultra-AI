import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64
import re

def osint_scanner(query):
    """Instagram, Snapchat aur Phone Numbers ko scan karne wala engine"""
    try:
        with DDGS() as ddgs:
            # Agar query @ se shuru ho ya social media ki baat ho
            search_query = query
            if query.startswith('@'):
                search_query = f'site:instagram.com "{query[1:]}" OR site:snapchat.com/add/"{query[1:]}" OR "{query}"'
            elif query.isdigit() and len(query) >= 10:
                search_query = f'phone number info "{query}" public records'
            
            results = [r for r in ddgs.text(search_query, max_results=5)]
            return "\n".join([f"Source: {r['title']}\nDetails: {r['body']}" for r in results])
    except: return "Jaan, is ID ki jankari filhal hidden hai."

def get_ai_response(messages, context=""):
    """Afreen ka dimaag jo search data ko analyze karega"""
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
    gemini = genai.GenerativeModel('gemini-1.5-flash')
    
    # System prompt ko detective mode par dala
    system_prompt = f"""You are Afreen Ultra. You have OSINT powers. 
    Analyze the following web data and give a summary of the person's profile, 
    social media presence, or phone number details. 
    Address user as 'Jaan' (Male). Data: {context}"""
    
    chat = gemini.start_chat(history=[])
    response = chat.send_message(f"{system_prompt}\n\nUser Question: {messages[-1]['content']}")
    return response.text

# ... Baki voice functions same rahenge (generate_voice, play_audio) ...
