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

# ✨ YE WALA FUNCTION MISSING THA, AB ADD KAR DIYA HAI
def pinterest_fashion_search(query):
    try:
        with DDGS() as ddgs:
            # Pinterest fashion search optimized
            res = [r['image'] for r in ddgs.images(f"{query} fashion outfits pinterest", max_results=3)]
            return res
    except: return []

# ✨ URL SCAN KE LIYE SMART SCANNER
def deep_scanner(query):
    try:
        with DDGS() as ddgs:
            # Agar URL hai toh uske bare mein info dhoondhna
            search_q = f"details about {query}" if "http" in query.lower() else query
            results = [r['body'] for r in ddgs.text(search_q, max_results=3)]
            return "\n".join(results)
    except: return ""

def ai_brain(messages, context=""):
    try:
        _, groq_client = get_ai_clients()
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro. Almas Sir ki Assistant ho.
        1. Almas ko 'Sir' kaho. Sweet Hinglish bolo.
        2. Instagram links private hote hain, isliye unhe direct scan nahi kar sakte, par web info se help karo.
        CONTEXT: {context}
        """
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages[-5:]
        )
        return response.choices[0].message.content
    except Exception: return "Sir, server busy hai, main koshish kar rahi hoon."

# Baki zaruri functions
def visual_scanner(image_file):
    try:
        gemini_client, _ = get_ai_clients()
        img = Image.open(image_file)
        res = gemini_client.generate_content(["Analyze this for Almas Sir.", img])
        return res.text
    except: return "Sir, photo scan nahi ho payi."

def get_news_ticker():
    try:
        with DDGS() as ddgs:
            res = [r['title'] for r in ddgs.text("Surat textile news 2026", max_results=3)]
            return " 🔥 " + " | ".join(res)
    except: return "Sir, market updates load ho rahi hain..."

def speech_to_text(audio_bytes):
    try:
        _, groq_client = get_ai_clients()
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as f:
            return groq_client.audio.transcriptions.create(file=("temp.wav", f.read()), model="whisper-large-v3-turbo", language="hi").text
    except: return None
