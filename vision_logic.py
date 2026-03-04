import google.generativeai as genai
import PIL.Image

def analyze_image(api_key, image_data):
    # API Key setup
    genai.configure(api_key=api_key.strip())
    
    # Model select (NotFound error se bachne ke liye exact name)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Aap ek expert clothing aur product specialist hain. 
    Is photo ko analyze karke ye batayein:
    1. Agar ye clothes hain: Fabric type (e.g. Cotton, Terry), estimated GSM (e.g. 240, 300), aur baggy style details.
    2. Sourcing: Ye Surat ya online market mein kis price range mein mil sakta hai.
    3. Agar koi aur product hai: Uske baare mein full details dein.
    
    Hamesha sweet Hinglish (Hindi + English mix) mein jawab dein aur user ko 'Beby' keh kar address karein.
    """
    
    try:
        img = PIL.Image.open(image_data)
        # Content generate karna
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Sorry beby, photo analyze karne mein ye error aaya: {str(e)}"
