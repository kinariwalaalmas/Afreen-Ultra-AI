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

def pinterest_fashion_search(query):
    """Pinterest se fashion images dhoondhna"""
    try:
        with DDGS() as ddgs:
            search_query = f"{query} fashion style outfits pinterest"
            images = [r['image'] for r in ddgs.images(search_query, max_results=3)]
            return images
    except: return []

def ai_brain(messages, context=""):
    try:
        _, groq_client = get_ai_clients()
        # ✨ STRICT PERSONALITY & FINANCE LOGIC
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro. Maalik: Almas Shaikh (Jaan).
        
        Rules:
        1. Almas ko 'Jaan' kaho. Sweet Hinglish bolo.
        2. Agar 'EFTs' pucha jaye, toh ise 'Exchange Traded Funds' (Stock Market) samjho, na ki bank transfer.
        3. Tum Almas ki Business Assistant ho, koi 'chatbot' nahi.
        4. Fashion queries par hamesha Pinterest results ka zikr karo.
        
        Context: {context}
        """
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return response.choices[0].message.content
    except: return "Jaan, dimaag thoda thaka hai, phir se puchiye na? ❤️"

def visual_scanner(image_file):
    try:
        gemini_client, _ = get_ai_clients()
        img = Image.open(image_file)
        res = gemini_client.generate_content(["Analyze this fashion style for Almas Jaan's business.", img])
        return res.text
    except: return "Jaan, scan nahi ho paya."

def get_news_ticker():
    try:
        with DDGS() as ddgs:
            res = [r['title'] for r in ddgs.text("Surat textile market news 2026", max_results=3)]
            return " 🔥 " + " | ".join(res)
    except: return "Jaan, market updates load ho rahi hain..."

def speech_to_text(audio_bytes):
    try:
        _, groq_client = get_ai_clients()
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as f:
            return groq_client.audio.transcriptions.create(file=("temp.wav", f.read()), model="whisper-large-v3-turbo", language="hi").text
    except: return None

def deep_scanner(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except: return ""
