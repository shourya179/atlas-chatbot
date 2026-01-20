from core.knowledge import get_domain_knowledge
from core.llm import call_llm
from typing import Dict,Any,List

def generate_plan(goals:Dict[str,Any])->List[str]:
    plan = []

    domain = goals.get("domain")
    technology = goals.get("technologies")

    plan.append("Clearly define the problem and target users.")

    if domain:
        domain_knowledge = get_domain_knowledge(domain)

        if domain_knowledge:
            plan.append(f"Key pain points in {domain}:")
            for p in domain_knowledge.get("pain_points", []):
                plan.append(f"- {p}")

            plan.append("Possible AI-driven solutions:")
            for s in domain_knowledge.get("solutions", []):
                plan.append(f"- {s}")

    if technology:
        plan.append(f"Design the system using {technology} best practices.")

    plan.append("Build an MVP focusing on one core feature.")
    plan.append("Test with real users and iterate.")

    return plan

def explain_plan(plan, goals):
    prompt = f"""
    You are an expert AI architect.

    User goal: {goals}

    Plan:
    {plan}

    Explain each step clearly and practically.
    """

    return call_llm(prompt)
