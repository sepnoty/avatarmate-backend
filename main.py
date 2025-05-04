from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stt import router as stt_router
from tts import router as tts_router
from llm import router as llm_router  # ✅ LLM route (DeepSeek or similar)

app = FastAPI()

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                   # Local development
        "http://localhost:5173",                   # Vite dev server
        "https://avatarmate.vercel.app"            # Vercel production URL (replace with your custom domain if needed)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root Route for testing
@app.get("/")
async def root():
    return {"message": "✅ AvatarMate Backend is live and running!"}

# ✅ Register API Routers
app.include_router(stt_router, prefix="/stt")    # 🎤 Speech-to-Text
app.include_router(tts_router, prefix="/tts")    # 🔊 Text-to-Speech
app.include_router(llm_router, prefix="/llm")    # 🧠 LLM / DeepSeek
