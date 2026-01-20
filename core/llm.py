import requests

def call_llm(input_data):
    """
    Accepts either:
    - list of messages [{role, content}, ...]
    - single prompt string
    """

    # ✅ Case 1: single prompt string (reflection, rewrite, planning)
    if isinstance(input_data, str):
        messages = [
            {"role": "user", "content": input_data}
        ]

    # ✅ Case 2: chat messages list
    elif isinstance(input_data, list):
        messages = []
        for m in input_data:
            if not m or not isinstance(m, dict):
                continue
            if not m.get("content"):
                continue
            messages.append({
                "role": m.get("role", "user"),
                "content": str(m.get("content"))
            })
    else:
        raise ValueError("call_llm expects str or list of messages")

    payload = {
        "model": "llama3",
        "messages": messages,
        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/chat",
        json=payload,
        timeout=120
    )

    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


def emotional_response(user_input):
    prompt = f"""
The user is expressing emotional distress.

User message:
"{user_input}"

Respond with empathy, warmth, and support.
Do not give medical advice.
"""
    return call_llm(prompt)
