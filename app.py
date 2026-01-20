from core.bot import chatbot
from core.intent import detect_intent
from core.dialogue import handle_intent
from core.entities import extract_entities
from core.executor import debug_state, handle_execution_control

bot = chatbot("Atlas")
bot.memory.load()

print("Atlas is online.\n")

control_commands = {"done", "next", "status", "change", "use tool"}
while True:

    raw_input = input("You: ").strip()
    user_input = raw_input.lower()

    control = None
    for cmd in control_commands:
        if user_input.startswith(cmd):
            control = cmd
            break

    # 1️⃣ Check if we are waiting for reflection feedback
    goals = bot.get_goals()
    
    if bot.memory.execution.get("expecting_reflection_input"):
        response = handle_execution_control(
            bot.memory,
            command=None,
            feedback=raw_input,
            goals=goals,
        )
        print(f"{bot.name}: {response}")
        continue
    print(debug_state(bot.memory))


# 2️⃣ Handle execution control commands (done, next, status, change)
    if control:
        response = handle_execution_control(bot.memory, control)
        print(f"{bot.name}: {response}")
        continue



    intent = detect_intent(user_input)
    context = bot.recent_context()

    entities = extract_entities(user_input)
    for key,value in entities.items():
        bot.remember_goal(key,value)
    
    goals = bot.get_goals()
    reply = handle_intent(intent, context,entities,goals,bot.memory)
    bot.remember_bot(reply)
    bot.remember_user(raw_input)
    

    
    if intent == "goodbye":
        break

    bot.memory.save()