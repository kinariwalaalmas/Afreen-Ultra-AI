import streamlit as st
import urllib.parse

def get_phone_action(command):
    cmd = command.lower()
    
    # 1. Call Logic
    if "call" in cmd:
        # Number extract karne ka simple tarika
        return f"tel:919876543210", "📞 Call Dialler khol rahi hoon, Jaan!"
        
    # 2. WhatsApp Logic
    if "whatsapp" in cmd:
        return "https://wa.me/", "💬 WhatsApp open kar rahi hoon, Jaan."
        
    # 3. Music/YouTube Logic
    if "song" in cmd or "play" in cmd:
        query = urllib.parse.quote(cmd.replace("play", ""))
        return f"https://www.youtube.com/results?search_query={query}", "🎵 Gaana dhoond rahi hoon, Jaan!"
        
    # 4. Alarm/Clock Shortcut (Android)
    if "alarm" in cmd or "timer" in cmd:
        return "intent://#Intent;action=android.intent.action.SET_ALARM;end", "⏰ Alarm setting khol rahi hoon!"

    return None, None
