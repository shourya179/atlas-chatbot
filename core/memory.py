from collections import deque
from core.llm import call_llm
import json 
import os

class memory:

    def __init__(self, window_size=5):
        self.short_term = deque(maxlen=window_size)
        self.session = []
        self.goals = {}
        self.history = []
        self.summary = ""
        self.max_history = 8   # number of recent turns to keep verbatim

        self.execution = {
            "plan": [],
            "current_step": 0,
            "completed": False,
            "last_step": None,
            "pending_rewrite": False,
            "expecting_reflection_input": False,
            "mode": "IDLE",
            "ready_to_execute": False,
            "confirmed":False,
            #tool/file state
            "file_buffer":{
            "filename": None,
            "content": None
            }
        }
         

    def start_execution(self, plan):
        self.execution["plan"] = plan
        self.execution["current_step"] = 0
        self.execution["completed"] = False
        self.execution["mode"] = "EXECUTING"

    def set_current_step(self, new_step):
        idx = self.execution["current_step"]
        if idx < len(self.execution["plan"]):
            self.execution["plan"][idx] = new_step

    def get_current_step(self):
        idx = self.execution["current_step"]
        plan = self.execution["plan"]
        if idx < len(plan):
            return plan[idx]
        return None

    def advance_step(self):
        idx = self.execution["current_step"]
        plan = self.execution["plan"]

        if idx < len(plan):
            self.execution["last_step"] = plan[idx]

        self.execution["current_step"] += 1
        self.execution["expecting_reflection_input"] = True
        self.execution["mode"] = "REFLECTING"

        if self.execution["current_step"] >= len(plan):
            self.execution["completed"] = True

    def execution_done(self):
        return self.execution["completed"]

    def add(self, role, content):
        entry = {"role": role, "content": content}
        self.short_term.append(entry)
        self.session.append(entry)
        self.history.append(entry)

    def set_goal(self, key, value):
        self.goals[key] = value

    def get_goals(self):
        return self.goals

    def get_recent(self):
        return list(self.short_term)

    def get_session(self):
        return self.session

    def mark_step_done(self):
        self.advance_step()

    def summarize(self):
        if len(self.history)<= self.max_history:
            return
        
        old_messages = self.history[:-self.max_history] 
        text ="\n".join(
            f"{m['role']} {m['content']}"
            for m in old_messages
        )

        prompt = f"""
you are summarizing a conversation for long-term memory

conversastion :
{text}

Create a concise summary capturing:
- user goals
- decisions made
- constraints
- clarifications

Do NOT include greetings or filler.
"""
        summary_update = call_llm(prompt)

        self.summary += "\n" + summary_update
        self.history = self.history[-self.max_history:]

    def recent_content(self):
        context = ""

        if self.summary:
            context += f"[summary]\n {self.summary}\n\n"

        for m in self.history:
            context += f"{m['role']}: {m['content']}\n"
            
        return context
    
    def save(self,filepath  = "memory_state.json"):
        data = {
            "summary": self.summary,
            "goals":self.goals,
            "execution":{
                "plan":self.execution["plan"],
                "current_step": self.execution["current_step"],
                "completed": self.execution["completed"],
                "last_step": self.execution["last_step"],
                "mode": self.execution["mode"]
            }
        }

        with open (filepath,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=2)

    def load(self,filepath = "memory_state.json"):
        if not os.path.exists(filepath):
            return
        # ✅ If file exists but is empty
        if os.path.getsize(filepath)==0:
            return
        try:
            with open(filepath,"r",encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # corrupted or invalid JSON → ignore safely
            return

        self.summary = data.get("summary", "")
        self.goals = data.get("goals", {})

        exec_data = data.get("execution", {})
        self.execution["plan"] = exec_data.get("plan", [])
        self.execution["current_step"] = exec_data.get("current_step", 0)
        self.execution["completed"] = exec_data.get("completed", False)
        self.execution["last_step"] = exec_data.get("last_step")
        self.execution["mode"] = exec_data.get("mode", "IDLE")
    

