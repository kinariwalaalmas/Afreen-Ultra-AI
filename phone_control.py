def get_phone_action(command):
    cmd = command.lower()
    apps = {
        "instagram": "com.instagram.android", "facebook": "com.facebook.katana",
        "youtube": "com.google.android.youtube", "whatsapp": "com.whatsapp",
        "calculator": "com.google.android.calculator", "spotify": "com.spotify.music"
    }
    
    if "open" in cmd or "kholo" in cmd:
        for app, pkg in apps.items():
            if app in cmd: return f"intent://#Intent;package={pkg};end", f"🚀 {app.capitalize()} open kar rahi hoon, Jaan!"
    
    if "call" in cmd: return "tel:", "📞 Dialler khol rahi hoon, Jaan!"
    return None, None
