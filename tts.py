from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse
import tempfile
import re
from TTS.api import TTS

router = APIRouter()

# Load the TTS model (CPU version)
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def clean_text(text):
    # Strip non-ASCII characters like emojis
    return re.sub(r'[^\x00-\x7F]+', '', text)

@router.post("/")
async def generate_tts(request: Request):
    try:
        data = await request.json()
        text = data.get("text")

        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="No text provided.")

        cleaned = clean_text(text)

        # Generate audio to temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tts_model.tts_to_file(text=cleaned, file_path=tmpfile.name)
            return FileResponse(
                tmpfile.name,
                media_type="audio/wav",
                filename="speech.wav"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")
