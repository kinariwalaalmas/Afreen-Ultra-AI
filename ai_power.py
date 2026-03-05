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
    """Afreen's Professional Personality"""
    try:
        _, groq_client = get_ai_clients()
        # ✨ IS PROMPT MEIN 'JAAN' KO 'SIR' SE BADAL DIYA HAI
        system_prompt = f"""
        Tumhara Naam: Afreen Ultra Pro. Tum Almas Shaikh (Sir) ki Personal AI Assistant ho.
        
        RULES:
        1. Almas Shaikh ko hamesha 'Sir' kehkar address karo. 
        2. Tumhari bhasha professional aur thodi sweet Hinglish honi chahiye.
        3. Business related sawalon ka jawab akalmand assistant ki tarah do.
        4. Agar 'EFTs' pucha jaye, toh Stock Market investment (Exchange Traded Funds) samjho.
        5. Kabhi mat kehna 'I am a chatbot'.
        
        CONTEXT: {context}
        """
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception: return "Sir, mera server thoda busy hai, main turant koshish karti hoon."

def pinterest_fashion_search(query):
    try:
        with DDGS() as ddgs:
            res = [r['image'] for r in ddgs.images(f"{query} fashion pinterest", max_results=3)]
            return res
    except: return []

def deep_scanner(query):
    try:
        with DDGS() as ddgs:
            res = [r['body'] for r in ddgs.text(query, max_results=2)]
            return "\n".join(res)
    except: return ""

def visual_scanner(image_file):
    try:
        gemini_client, _ = get_ai_clients()
        img = Image.open(image_file)
        prompt = "Tum Afreen ho. Is style ko analyze karo aur Almas Sir ko business advice do."
        response = gemini_client.generate_content([prompt, img])
        return response.text
    except: return "Sir, photo scan nahi ho payi."

def get_news_ticker():
    try:
        with DDGS() as ddgs:
            res = [r['title'] for r in ddgs.text("Surat textile market news 2026", max_results=3)]
            return " 🔥 " + " | ".join(res)
    except: return "Sir, market updates load ho rahi hain..."

def speech_to_text(audio_bytes):
    try:
        _, groq_client = get_ai_clients()
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as f:
            return groq_client.audio.transcriptions.create(file=("temp.wav", f.read()), model="whisper-large-v3-turbo", language="hi").text
    except: return None
