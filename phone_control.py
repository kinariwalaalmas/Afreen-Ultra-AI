import streamlit as st
import urllib.parse

def get_phone_action(command):
    cmd = command.lower()
    
    # --- 1. Popular Apps ka Data (Package Names) ---
    # Android par package name se koi bhi app khul jati hai
    apps = {
        "instagram": "com.instagram.android",
        "facebook": "com.facebook.katana",
        "snapchat": "com.snapchat.android",
        "telegram": "org.telegram.messenger",
        "youtube": "com.google.android.youtube",
        "chrome": "com.android.chrome",
        "maps": "com.google.android.apps.maps",
        "calculator": "com.google.android.calculator",
        "spotify": "com.spotify.music",
        "gmail": "com.google.android.gm",
        "twitter": "com.twitter.android",
        "x": "com.twitter.android",
        "netflix": "com.netflix.mediaclient",
        "paytm": "net.one97.paytm",
        "phonepe": "com.phonepe.app"
    }

    # --- 2. App Opening Logic ---
    if "open" in cmd or "kholo" in cmd:
        for app_name, package in apps.items():
            if app_name in cmd:
                # Android Intent Link
                url = f"intent://#Intent;package={package};end"
                return url, f"🚀 {app_name.capitalize()} open kar rahi hoon, Jaan!"
        
        # Agar list mein nahi hai, toh generic try
        clean_name = cmd.replace("open", "").replace("kholo", "").strip()
        if clean_name:
            # Common pattern try karna
            url = f"intent://#Intent;package=com.{clean_name};end"
            return url, f"🚀 {clean_name.capitalize()} open karne ki koshish kar rahi hoon, Jaan!"

    # --- 3. Calling & WhatsApp (Existing) ---
    if "call" in cmd:
        return "tel:", "📞 Dialler open kar rahi hoon, Jaan!"
        
    if "whatsapp" in cmd:
        return "https://wa.me/", "💬 WhatsApp open kar rahi hoon, Jaan."
        
    if "play" in cmd or "gaana" in cmd:
        query = urllib.parse.quote(cmd.replace("play", "").replace("gaana", ""))
        return f"https://www.youtube.com/results?search_query={query}", "🎵 YouTube par dhoond rahi hoon!"

    return None, None
