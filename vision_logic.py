import google.generativeai as genai
import PIL.Image

def analyze_image(api_key, image_data):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Act as an expert shopping assistant and fabric specialist. 
    Analyze this image in detail:
    1. Agar ye kapde (clothes) hain: Batayein ki ye kis type ka fabric hai, iska estimated GSM kitna ho sakta hai, aur iska styling kaisa hai.
    2. Sourcing: Ye Surat ya online market mein kahan mil sakta hai aur estimated price kya hogi.
    3. Agar ye koi aur product hai: Uske specs aur use batayein.
    Answer in sweet Hinglish (Hindi + English mix) and be very helpful.
    """
    
    img = PIL.Image.open(image_data)
    response = model.generate_content([prompt, img])
    return response.text
