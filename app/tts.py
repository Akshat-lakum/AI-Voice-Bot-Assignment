from gtts import gTTS
import os
import uuid

def text_to_speech(text):
    """
    Converts text to an MP3 file and returns the filename.
    """
    try:
        # Generate a unique filename so different users don't clash
        filename = f"response_{uuid.uuid4().hex}.mp3"
        file_path = os.path.join("static", filename)
        
        # Ensure static folder exists
        os.makedirs("static", exist_ok=True)

        tts = gTTS(text=text, lang='en')
        tts.save(file_path)
        
        return filename
    except Exception as e:
        print(f"TTS Error: {e}")
        return None