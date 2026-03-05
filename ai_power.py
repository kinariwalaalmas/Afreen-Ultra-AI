import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
from PIL import Image

def get_ai_clients():
    """API Keys setup"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception:
        return None, None

def ai_brain(messages, context=""):
    """Afreen's Intelligence"""
    try:
        _, groq_client = get_ai_clients()
        system_prompt = f"You are Afreen Ultra. Owner: Almas Shaikh. Speak sweet Hinglish. Context: {context}"
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].message.content
    except: return "Jaan, dimaag thoda thaka hua hai, phir se puchiye."

def visual_scanner(image_file):
    """Fashion Recognition"""
    try:
        gemini_client, _ = get_ai_clients()
        img = Image.open(image_file)
        response = gemini_client.generate_content(["Tum Afreen ho. Is fashion style ko Almas Shaikh ke liye analyze karo.", img])
        return response.text
    except: return "Jaan, photo scan nahi ho payi."

def get_news_ticker():
    """Market Updates"""
    try:
        with DDGS() as ddgs:
            res = [r['title'] for r in ddgs.text("Surat textile baggy clothing market news 2026", max_results=3)]
            return " 🔥 " + " | ".join(res)
    except: return "Jaan, market updates load ho rahi hain..."

def speech_to_text(audio_bytes):
    """Voice Translation"""
    try:
        _, groq_client = get_ai_clients()
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as file:
            return groq_client.audio.transcriptions.create(
                file=("temp.wav", file.read()),
                model="whisper-large-v3-turbo",
                language="hi"
            ).text
    except: return None

def deep_scanner(query):
    """Web Search"""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            images = [r['image'] for r in ddgs.images(query, max_results=1)]
            return "\n".join(results), images
    except: return "", []
