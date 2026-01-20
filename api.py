from fastapi import FastAPI
from core.bot import chatbot
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()
bot = chatbot("Atlas")
bot.memory.load()

class ChatRequest(BaseModel):
    message: Optional[str] = ""

@app.post("/chat")
def chat(req: ChatRequest):
    reply = bot.handle(req.message or "")
    bot.memory.save()
    return {"reply": reply}

@app.get("/")
def root():
    return {"status": "Atlas is running"}

@app.get("/health")
def health():
    return {"status": "ok", "model": "llama3"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
