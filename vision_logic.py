import google.generativeai as genai
import PIL.Image

def analyze_image(api_key, image_data):
    genai.configure(api_key=api_key.strip())
    model = genai.GenerativeModel('gemini-1.5-flash')
    img = PIL.Image.open(image_data)
    prompt = "Analyze this in Hinglish. If it's clothes, mention GSM, fabric, and Surat sourcing. Address user as 'Beby' with masculine grammar (Kaise ho)."
    return model.generate_content([prompt, img]).text
