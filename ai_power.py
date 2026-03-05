import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
from PIL import Image
import os

# 1. API Clients
def get_ai_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

# 2. ✨ PINTEREST FASHION SEARCH (Naya Feature)
def pinterest_fashion_search(query):
    """Pinterest se best fashion photos dhoondhna"""
    try:
        with DDGS() as ddgs:
            # Query ko Pinterest ke liye optimize karna
            pinterest_query = f"{query} fashion outfits pinterest"
            # Images dhoondhna
            images = [r['image'] for r in ddgs.images(pinterest_query, max_results=3)]
            return images
    except Exception:
        return []

# 3. 🧠 SMART AI BRAIN (Financial & Fashion Expert)
def ai_brain(messages, context=""):
    try:
        _, groq_client = get_ai_clients()
        # Updated System Prompt
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro. Maalik: Almas Shaikh (Jaan).
        Tum Almas ki Smart Assistant ho.
        
        Rules:
        1. 'Jaan' kehkar address karo. Sweet Hinglish mein bolo.
        2. Agar financial sawal ho (EFTs, Stocks), toh accurate jawab do.
        3. Agar fashion ka sawal ho, toh Pinterest se photos dhoondh kar do.
        4. Kabhi mat kehna 'I am a chatbot'.
        
        Context: {context}
        """
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception:
        return "Jaan, main abhi thoda confuse hoon. Phir se puchiye na? ❤️"

# 4. Baki ke Zaruri Functions (Same as before)
def visual_scanner(image_file):
    try:
        gemini_client, _ = get_ai_clients()
        img = Image.open(image_file)
        prompt = "Tum Afreen ho. Is fashion style ya fabric ko analyze karo aur Almas Jaan ko business advice do."
        response = gemini_client.generate_content([prompt, img])
        return response.text
    except Exception: return "Jaan, photo scan nahi ho payi."

def get_news_ticker():
    try:
        with DDGS() as ddgs:
            res = [r['title'] for r in ddgs.text("Surat textile market baggy clothing trends 2026", max_results=3)]
            return " 🔥 " + " | ".join(res)
    except Exception: return "Jaan, market updates aa rahi hain..."

def speech_to_text(audio_bytes):
    try:
        _, groq_client = get_ai_clients()
        with open("temp_voice.wav", "wb") as f: f.write(audio_bytes)
        with open("temp_voice.wav", "rb") as file:
            transcription = groq_client.audio.transcriptions.create(file=("temp_voice.wav", file.read()), model="whisper-large-v3-turbo", language="hi")
        os.remove("temp_voice.wav")
        return transcription.text
    except Exception: return None

# 5. SMART WEB SEARCH (Financial & General)
def deep_scanner(query):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except Exception: return ""
