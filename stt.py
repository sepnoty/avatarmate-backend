from fastapi import APIRouter, File, UploadFile
import whisper
import os
import tempfile

router = APIRouter()
model = whisper.load_model("base")  # or use "small", "medium", "large"

@router.post("/")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = model.transcribe(tmp_path)
        return {"text": result["text"]}
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.remove(tmp_path)
