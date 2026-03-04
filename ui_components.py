def render_plus_menu():
    with st.popover("＋"):
        st.write("### Tools")
        audio = mic_recorder(start_prompt="Record 🎤", stop_prompt="Done ✅", key='mic')
        st.divider()
        
        # Quick Shortcuts for Phone
        st.write("🚀 Quick Launch")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📞 Call", "tel:")
            st.link_button("⏰ Alarm", "intent://#Intent;action=android.intent.action.SET_ALARM;end")
        with col2:
            st.link_button("💬 WA", "https://wa.me/")
            st.link_button("🎶 Music", "https://www.youtube.com")
            
    return audio, None, None # Ticker/Photo logic pehle jaisa
