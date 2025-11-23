import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# UPDATED MODEL NAME HERE:
model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_intent(user_text):
    """
    Analyzes user text to determine Intent.
    """
    prompt = f"""
    You are the NLU engine for a customer service voice bot.
    User said: "{user_text}"
    
    Classify the intent into one of these categories:
    - balance_check (if asking for money, account balance, savings)
    - faq_hours (if asking when we are open)
    - faq_location (if asking where we are located)
    - faq_contact (if asking for email or phone support)
    - greeting (hello, hi)
    - goodbye (bye, exit)
    - unknown (anything else)

    Return ONLY a JSON object like this:
    {{
      "intent": "balance_check",
      "reply_text": "placeholder"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up json formatting
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"NLU Error: {e}")
        return {"intent": "unknown", "reply_text": "I didn't understand that."}

def generate_smart_reply(user_text):
    try:
        response = model.generate_content(f"You are a helpful customer support assistant. Reply briefly to: {user_text}")
        return response.text.strip()
    except:
        return "I am currently having trouble thinking."