from core.llm import call_llm

def rewrite_step(step, goals, feedback):
    prompt = f"""
You are improving a single step in a plan.

User goals:
{goals}

Current step:
{step}

User feedback:
{feedback}

Task:
Rewrite the step to be clearer, more actionable, and concise.
Do NOT add new steps.
Return only the rewritten step.
"""
    return call_llm(prompt)
