from core.reflection import reflect_with_llm
from core.rewrite import rewrite_step
from core.tool_executor import execute_tool
from core.tool_selector import suggestion_tool_llm


def handle_execution_control(memory, command=None, feedback=None, goals=None):
    e = memory.execution
    mode = e["mode"]

    # =========================
    # 1️⃣ REFLECTION MODE
    # =========================
    if mode == "REFLECTING":
        if feedback and feedback.strip().lower() in {"ok", "yes"}:
            e["expecting_reflection_input"] = False
            e["mode"] = "EXECUTING"
            return reflect_with_llm(memory, feedback)

        return "Please briefly reflect on this step, or say 'ok' to continue."

    # =========================
    # 2️⃣ REWRITE MODE
    # =========================
    if mode == "REWRITING":
        if not feedback:
            return "Tell me what you want to change in this step."

        step = memory.get_current_step()
        improved = rewrite_step(step, goals, feedback)
        memory.set_current_step(improved)

        e["pending_rewrite"] = False
        e["mode"] = "EXECUTING"
        return f"Updated step:\n{improved}"

    # =========================
    # 3️⃣ IDLE MODE → DO NOTHING
    # =========================
    if mode == "IDLE":
        return None

    # =========================
    # 4️⃣ STATUS
    # =========================
    if command == "status":
        e = memory.execution

    return (
        "📊 Status\n"
        f"- Mode: {e.get('mode', 'UNKNOWN')}\n"
        f"- Plan active: {'Yes' if e.get('plan') else 'No'}\n"
        f"- Current step: {memory.get_current_step() or 'None'}\n"
        f"- Pending rewrite: {e.get('pending_rewrite', False)}"
    )


    # =========================
    # 5️⃣ DONE / NEXT
    # =========================
    if command in {"done", "next"}:
        memory.advance_step()
        return "Step completed. Briefly reflect or say 'ok' to continue."

    # =========================
    # 6️⃣ CHANGE STEP
    # =========================
    if command == "change":
        e["pending_rewrite"] = True
        e["mode"] = "REWRITING"
        return "What would you like to improve or clarify?"

    # =========================
    # 7️⃣ TOOL USAGE
    # =========================
    if command == "use tool":
        step = memory.get_current_step()

        tool = suggestion_tool_llm(step)

        if not tool:
            return (
                "I don’t think a tool is needed for this step.\n"
                "You can continue manually or say 'next'."
        )

        result = execute_tool(tool, step)

        return (
            f"I used the tool **{tool}** for this step.\n\n"
            f"Result:\n{result}\n\n"
            "Say 'next' to continue, or 'change' to refine this step."
        )
    
# =========================
# 🔍 SUGGEST TOOL (PASSIVE)
# =========================
    step = memory.get_current_step()
    tool = suggestion_tool_llm(step)

    if tool:
        return (
            f"Current step:\n{step}\n\n"
            f"I can use the tool **{tool}** to help with this.\n"
            "Say 'use tool' to proceed, or 'next' to continue manually."
        )
    # =========================
    # 8️⃣ DEFAULT
    # =========================
    return "Say 'next' when you’re ready to continue."




# =========================
# 🔧 DEBUG (DEV ONLY)
# =========================
def debug_state(memory):
    e = memory.execution
    return (
        f"[STATE]\n"
        f"mode: {e['mode']}\n"
        f"step: {e['current_step']}\n"
        f"pending_rewrite: {e['pending_rewrite']}\n"
    )
