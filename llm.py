from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()
router = APIRouter()

class MessageRequest(BaseModel):
    message: str
    tone: str

@router.post("/")
async def get_ai_reply(data: MessageRequest):
    system_prompt = f"You are a {data.tone} and emotionally supportive AI companion. Reply kindly and warmly."

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": data.message}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return {"reply": response.json()["choices"][0]["message"]["content"].strip()}
    except Exception as e:
        print("LLM API Error:", e)
        raise HTTPException(status_code=500, detail="AI could not respond.")
