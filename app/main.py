from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from app import dialog
import os
import shutil

app = FastAPI(title="Voice Bot API")

# Serve the static folder so we can listen to the generated MP3s via URL
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/process-voice")
async def process_voice(file: UploadFile = File(...)):
    """
    Endpoint to receive audio file, process it, and return audio response.
    """
    temp_filename = f"temp_{file.filename}"
    
    try:
        # Save uploaded file temporarily
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process the file through our AI pipeline
        result = dialog.process_voice_interaction(temp_filename)
        
        # Return structured JSON response
        return {
            "status": "success",
            "data": result,
            "audio_url": f"/static/{result['audio_response']}" if result['audio_response'] else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.get("/")
def home():
    return {"message": "Voice Bot API is running. Use POST /process-voice to interact."}