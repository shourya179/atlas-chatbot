from core.memory import memory
from core.dialogue import handle_intent
from core.entities import extract_entities
from core.executor import handle_execution_control
from core.intent import detect_intent
from core.llm import call_llm, emotional_response
from core.file_parser import parse_file_command
from core.tool_executor import execute_tool

class chatbot:
    def __init__(self, name):
        self.name = name
        self.memory = memory()

    def handle(self, raw_input: str):
        user_input = raw_input.lower()
        control_commands = {"done", "next", "status", "change", "use tool"}

        # =========================
        # 🔹 FILE CREATION (HARD GATE)
        # =========================
        filename, content = parse_file_command(raw_input)
        buffer = self.memory.execution["file_buffer"]

        if filename:
            buffer["filename"] = filename
            return f"File name set to '{filename}'. What should I write in it?"

        if content and buffer["filename"]:
            buffer["content"] = content
            result = execute_tool(
                "write_file",
                {
                    "filename": buffer["filename"],
                    "content": buffer["content"]
                }
            )
            buffer["filename"] = None
            buffer["content"] = None
            return result

        # =========================
        # 🔹 EXECUTION MODES
        # =========================
        if self.memory.execution.get("mode") in {"REFLECTING", "REWRITING"}:
            return handle_execution_control(
                self.memory,
                command=None,
                feedback=raw_input,
                goals=self.memory.goals
            )

        # =========================
        # 🔹 CONTROL COMMANDS
        # =========================
        for cmd in control_commands:
            if user_input.startswith(cmd):
                return handle_execution_control(
                    self.memory,
                    command=cmd,
                    goals=self.memory.goals
                )

        # =========================
        # 🔹 NORMAL CHAT
        # =========================
        self.memory.add("user", raw_input)

        intent = detect_intent(user_input)
        context = self.memory.recent_content()

        entities = extract_entities(user_input)
        for k, v in entities.items():
            self.memory.goals[k] = v

        agent_response = handle_intent(
            intent=intent,
            context=context,
            entities=entities,
            goals=self.memory.goals,
            memory=self.memory
        )

        if agent_response:
            self.memory.add("assistant", agent_response)
            return agent_response

        if intent == "emotion":
            reply = emotional_response(raw_input)
            self.memory.add("assistant", reply)
            return reply

        # =========================
        # 🔹 LLM FALLBACK (NO FILE CLAIMS)
        # =========================
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Atlas, a local AI assistant. "
                    "You can create and manage REAL files ONLY using tools "
                    "inside the project's 'workspace' folder. "
                    "Never claim file creation unless a tool confirms it."
                )
            }
        ]

        for m in self.memory.history[-6:]:
            messages.append(m)

        messages.append({"role": "user", "content": raw_input})

        reply = call_llm(messages)
        self.memory.add("assistant", reply)
        return reply
