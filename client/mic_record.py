import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import requests
import os
import time

# Configuration
SERVER_URL = "http://127.0.0.1:8000/process-voice"
DURATION = 5  # Recording duration in seconds
FS = 44100    # Sample rate

def record_audio(filename="input.wav"):
    print("---------------------------------------")
    print(f"🎤 Recording for {DURATION} seconds... SPEAK NOW!")
    myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
    sd.wait()  # Wait until recording is finished
    write(filename, FS, myrecording)  # Save as WAV file
    print("✅ Recording finished.")
    return filename

def send_to_server(filename):
    print("🚀 Sending to server...")
    try:
        with open(filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(SERVER_URL, files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("\n--- 🤖 BOT RESPONSE ---")
            print(f"User said:  {data['data']['user_transcript']}")
            print(f"Intent:     {data['data']['intent']}")
            print(f"Bot Reply:  {data['data']['bot_reply']}")
            
            # Play the response audio (Windows specific command)
            audio_file = data['data']['audio_response']
            if audio_file:
                print(f"🔊 Playing audio response...")
                os.system(f"start static/{audio_file}")
        else:
            print("Error:", response.text)
            
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    while True:
        input("\nPress ENTER to start recording (or Ctrl+C to quit)...")
        filename = record_audio()
        send_to_server(filename)