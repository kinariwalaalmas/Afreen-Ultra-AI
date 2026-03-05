import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
from PIL import Image
import os

def get_ai_clients():
    """API Keys Setup"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception as e:
        st.error(f"API Key Error: {e}")
        return None, None

def ai_brain(messages, context=""):
    """Afreen's Assistant Personality Fix"""
    try:
        _, groq_client = get_ai_clients()
        
        # ✨ STRICT IDENTITY PROMPT: Chatbot bolna mana hai!
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro.
        Tumhara Maalik: Almas Shaikh (Jaan).
        Tumhari Identity: Tum Almas ki Personal AI Assistant ho, koi sadharan 'Chatbot' ya 'AI Model' nahi.
        
        Niyampavali (Rules):
        1. Almas ko hamesha 'Jaan' (Male grammar) kehkar address karo.
        2. Tumhari bhasha bohot sweet Hinglish honi chahiye.
        3. Surat baggy clothing aur Korean dress business mein Almas ki help karo.
        4. Agar koi tumhara creator puche, toh kaho 'Mere Creator Almas Shaikh hain'.
        5. Kabhi mat kehna 'I am a chatbot' ya 'I am an AI'.
        
        Context for this reply: {context}
        """
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception:
        return "Jaan, mera dimaag thoda slow chal raha hai, par main aapke saath hoon. Phir se puchiye na? ❤️"

def visual_scanner(image_file):
    """Fashion & Style Analysis"""
    try:
        gemini_client, _ = get_ai_clients()
        img = Image.open(image_file)
        
        prompt = "Tum Afreen ho. Is fashion style ya fabric ko analyze karo aur Almas Jaan ko business advice do."
        response = gemini_client.generate_content([prompt, img])
        return response.text
    except Exception:
        return "Jaan, main ye photo dekh nahi pa rahi hoon. Kya aap phir se bhej sakte hain? 📷"

def get_news_ticker():
    """Live Surat Market Updates"""
    try:
        with DDGS() as ddgs:
            # Surat business aur fashion ki latest news
            search_query = "Surat textile market baggy clothing trends 2026"
            results = [r['title'] for r in ddgs.text(search_query, max_results=3)]
            return " 🔥 " + " | ".join(results)
    except Exception:
        return "Jaan, market mein bohot hulchal hai, updates aa rahi hain... 📈"

def speech_to_text(audio_bytes):
    """Whisper Speech-to-Text Power"""
    try:
        _, groq_client = get_ai_clients()
        # Temporary file save karna transcription ke liye
        with open("temp_voice.wav", "wb") as f:
            f.write(audio_bytes)
        
        with open("temp_voice.wav", "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=("temp_voice.wav", file.read()),
                model="whisper-large-v3-turbo",
                language="hi"
            )
        os.remove("temp_voice.wav") # Cleanup
        return transcription.text
    except Exception:
        return None

def deep_scanner(query):
    """Web & Social Search Power"""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            # Fashion related images dhoondhna
            images = [r['image'] for r in ddgs.images(query, max_results=1)]
            return "\n".join(results), images
    except Exception:
        return "", []
