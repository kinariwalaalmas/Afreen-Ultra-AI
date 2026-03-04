import google.generativeai as genai
import PIL.Image

def analyze_image(api_key, image_data):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    img = PIL.Image.open(image_data)
    prompt = "Analyze GSM, fabric, and Surat sourcing in Hinglish. Use masculine grammar for 'Jaan'."
    return model.generate_content([prompt, img]).text
