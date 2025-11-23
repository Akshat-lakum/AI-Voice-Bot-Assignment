import os
import time
from app import stt, nlu, tts
from app import db

def process_voice_interaction(audio_file_path):
    start_time = time.time() # Start timer

    response_data = {
        "user_transcript": "",
        "intent": "",
        "bot_reply": "",
        "audio_response": None
    }

    # 1. Speech to Text
    transcript = stt.transcribe_audio(audio_file_path)
    if not transcript:
        response_data["bot_reply"] = "I could not hear you properly."
        response_data["audio_response"] = tts.text_to_speech(response_data["bot_reply"])
        return response_data
    
    response_data["user_transcript"] = transcript

    # 2. NLU
    nlu_result = nlu.analyze_intent(transcript)
    intent = nlu_result.get("intent", "unknown")
    response_data["intent"] = intent

    # 3. Logic
    reply_text = ""
    if intent == "balance_check":
        balance = db.get_user_balance("John Doe")
        reply_text = f"Your current account balance is ${balance}."
    elif intent in ["faq_hours", "faq_location", "faq_contact"]:
        keyword = intent.split("_")[1]
        reply_text = db.get_faq_answer(keyword) or "I am sorry, I don't have that information."
    elif intent == "greeting":
        reply_text = "Hello! How can I help you today?"
    elif intent == "goodbye":
        reply_text = "Goodbye! Have a great day."
    else:
        reply_text = nlu.generate_smart_reply(transcript)

    response_data["bot_reply"] = reply_text

    # 4. TTS
    audio_filename = tts.text_to_speech(reply_text)
    response_data["audio_response"] = audio_filename
    
    # 5. LOGGING (New!)
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    db.log_interaction(transcript, intent, reply_text, duration)

    return response_data