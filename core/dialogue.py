from core.planner import generate_plan

def handle_intent(intent, context, entities=None, goals=None, memory=None):
    entities = entities or {}
    goals = goals or {}

    # 🔒 Agent must stay silent until explicitly confirmed
    if intent == "build_project":
        if not memory.execution.get("confirmed", False):
            return None  # ← THIS IS THE KEY LINE

        # ✅ Only now start execution
        if not memory.execution["plan"]:
            plan = generate_plan(goals)
            memory.start_execution(plan)

        return f"Current step:\n{memory.get_current_step()}"

    return None
