from core.llm import call_llm
from core.tools import list_tools

def suggestion_tool_llm(step:str):
    tools = list_tools()

    tool_descriptions = "\n".join(
        f"- {name} : {info['description']}"
        for name,info in tools.items()
    )
    prompt = f"""
You are a tool-selection engine.

Current task:
{step}

Available tools:
{tool_descriptions}

Rules:
- Reply with EXACTLY ONE word.
- The word must be one of the tool names above.
- If no tool is needed, reply with: none
- Do NOT explain your choice.

Respond with ONLY the tool name.
"""


    response = call_llm(prompt)

    if not response:
        return None

    response = response.strip().lower()
    response = response.replace("tool:","").strip()
    response = response.split()[0]

    if response == "none":
        return None
    
    return response if response in tools else None
