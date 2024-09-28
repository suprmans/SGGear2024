import google.generativeai as genai

genai.configure(api_key="<GET API KEY>")
model = genai.GenerativeModel('gemini-1.5-flash')

def gemini_response(ask_gemini):
    model = genai.GenerativeModel('gemini-1.5-flash')
    gemini_response = model.generate_content(ask_gemini)
    return gemini_response