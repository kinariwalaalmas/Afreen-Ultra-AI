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
    try:
        _, groq_client = get_ai_clients()
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro. Tum Almas Sir ki Personal Assistant ho.
        
        RULES:
        1. Almas ko 'Sir' kaho. Sweet Hinglish bolo.
        2. Agar koi URL (Instagram/Web) scan na ho paye, toh Sir ko batao ki ye security ki wajah se 'Locked' hai aur unse screenshot maango.
        3. EFTs = Exchange Traded Funds.
        
        CONTEXT: {context}
        """
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages[-5:]
        )
        return response.choices[0].message.content
    except Exception: return "Sir, server thoda busy hai, main koshish kar rahi hoon."

# ✨ NEW SMART SCANNER FOR URLs
def deep_scanner(query):
    try:
        with DDGS() as ddgs:
            # Agar URL hai, toh uske baare mein general search karo
            if "http" in query.lower():
                search_query = f"site info and details for {query}"
            else:
                search_query = query
            
            results = [r['body'] for r in ddgs.text(search_query, max_results=3)]
            return "\n".join(results)
    except: return ""

def pinterest_fashion_search(query):
    try:
        with DDGS() as ddgs:
            res = [r['image'] for r in ddgs.images(f"{query} fashion pinterest", max_results=3)]
            return res
    except: return []

# Keep visual_scanner, get_news_ticker, speech_to_text same as before
