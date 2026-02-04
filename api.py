from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from core.bot import chatbot
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time

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

@app.post("chat-stream")

def chat_stream(request:dict):
    user_input = request.get("massage","")

    def event_gentrator():
        # 🔴 TEMP: simulate streaming
        # Later this will come from the LLM
        response = bot.handle(user_input)

        for word in response.split():
            yield f"data:{word}\n\n"
            time.sleep(.05)
        yield "data:[END]\n\n"
    return StreamingResponse(
        event_gentrator(),
        media_type="text/event-steam"
    )