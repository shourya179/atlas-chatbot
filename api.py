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
@app.post("/chat-stream")
def chat_stream(req: ChatRequest):

    def event_generator():
        try:
            response = bot.handle(req.message)
            

            if not response:
                yield "data: ⚠️ Empty response\n\n"
                return

            for word in response.split():
                yield f"data: {word}\n\n"
                time.sleep(0.05)

            return{"response":response}

        except Exception as e:
            # 🔥 CRITICAL: never let generator crash
            yield f"data: ⚠️ LLM error: {str(e)}\n\n"

        finally:
            # 🔥 ALWAYS end the stream
            yield "data: [END]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
