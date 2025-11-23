import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def transcribe_audio(file_path):
    """
    Uploads audio to Gemini 2.0 Flash and requests a transcription.
    """
    if not os.path.exists(file_path):
        print("Error: Audio file not found.")
        return None

    try:
        print(f"Uploading {file_path} to Gemini...")
        
        # 1. Upload the audio file
        audio_file = genai.upload_file(path=file_path, mime_type="audio/wav")
        
        # 2. Wait for processing
        while audio_file.state.name == "PROCESSING":
            time.sleep(1)
            audio_file = genai.get_file(audio_file.name)

        if audio_file.state.name == "FAILED":
            print("Audio processing failed.")
            return None

        # 3. Generate content
        print("Generating transcript...")
        # UPDATED MODEL NAME HERE:
        model = genai.GenerativeModel("gemini-2.0-flash") 
        response = model.generate_content(
            [audio_file, "Please transcribe this audio file exactly as spoken. Do not add any commentary."]
        )
        
        # 4. Clean up
        genai.delete_file(audio_file.name)

        return response.text.strip()

    except Exception as e:
        print(f"STT Error: {e}")
        return None