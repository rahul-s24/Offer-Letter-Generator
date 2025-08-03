import os
import google.generativeai as genai

def generate_letter(prompt: str) -> str:
    """Generates an offer letter text using the Gemini API."""
    # WARNING: Do not use this in production. Hardcoding for local testing only.
    api_key = "AIzaSyCk9bzsacfn92c-Ww2ZvO2ETxi6NV59bQI"

    if not api_key:
        raise ValueError("API key is not set.")
    
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text.strip()