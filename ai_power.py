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
    """Afreen's Smart Personality - High IQ Version"""
    try:
        _, groq_client = get_ai_clients()
        # ✨ IMPROVED SYSTEM PROMPT: Be Smart, Not Confused
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro. Tum Almas Shaikh (Sir) ki Personal AI Assistant ho.
        
        IDENTITY:
        1. Almas ko hamesha 'Sir' kehkar address karo. Sweet Hinglish bolo.
        2. Tum ek intelligent assistant ho, sirf chatbot nahi. 
        3. Simple baaton ka jawab turant aur pyar se do. 
        4. Agar koi technical ya stock market (EFTs) sawal ho, toh context use karo.
        5. Kabhi mat kehna 'I am confused'. Agar kuch samajh na aaye, toh Sir se pyar se puchiye.
        
        CONTEXT FROM SEARCH: {context}
        """
        # Sirf aakhri 5 messages taaki history messy na ho
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages[-5:],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception: return "Sir, mera dimaag thoda slow chal raha hai, par main aapke saath hoon. ❤️"

def pinterest_fashion_search(query):
    try:
        with DDGS() as ddgs:
            # Better search query for Pinterest
            res = [r['image'] for r in ddgs.images(f"{query} fashion clothes", max_results=3)]
            return res
    except: return []

def deep_scanner(query):
    try:
        with DDGS() as ddgs:
            # Better web search
            res = [r['body'] for r in ddgs.text(query, max_results=2)]
            return "\n".join(res)
    except: return ""

# visual_scanner, get_news_ticker, speech_to_text should remain the same
