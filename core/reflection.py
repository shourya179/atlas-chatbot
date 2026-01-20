from core.llm import call_llm

def reflect_with_llm(memory, user_feedback=None):
    step = memory.execution.get("last_step")

    if not step:
        return None

    prompt = f"""
You are an expert assistant helping a user execute a plan step-by-step.

Current step:
{step}

User feedback (if any):
{user_feedback}

Your task:
1. Decide if this step is sufficiently clear and complete.
2. If yes, briefly explain why.
3. If not, suggest a clearer or improved version of the step.

Be concise and practical.
"""

    return call_llm(prompt)
