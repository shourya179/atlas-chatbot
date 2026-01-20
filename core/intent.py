import json
from typing import Dict, List
from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/intents.json") as f:
    INTENTS: Dict[str, List[str]] = json.load(f)

intent_embedding = {}
for intent,examples in INTENTS.items():
    intent_embedding[intent] = model.encode (examples,convert_to_tensor=True)

def detect_intent(user_input: str) -> str:
    text = user_input.lower()
    tokens = set(re.findall(r"\b\w+\b", text))

    EMOTIONS = {
        "happy", "sad", "lonely", "excited",
        "angry", "upset", "depressed"
    }


    EXIT_WORDS = {"bye", "goodbye", "exit", "quit"}
    GREETINGS = {"hello", "hi", "hey"}
    AFFIRMATIONS = {"yes", "yeah", "yep", "sure", "ok"}

    # 1️⃣ Emotion first (highest priority)
    if tokens & EMOTIONS:
        return "emotion"

    # 2️⃣ Build project 
    if "build" in tokens or "create" in tokens or "make" in tokens:
        return "build_project"

    # 3️⃣ Explicit goodbye only
    if tokens & EXIT_WORDS:
        return "goodbye"

    # 4️⃣ Greeting
    if tokens & GREETINGS:
        return "greeting"

    # 5️⃣ Affirmation
    if tokens & AFFIRMATIONS:
        return "continue"
    
    return "unknown"